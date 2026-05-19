from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from .forms import CatalogForm, StockForm
from .models import CatalogMod, StockMod

def pharmagen(request):
    return render(request, 'pharma/pages/pharmagen.html')

def list_view(request):
    query_secondary = request.GET.get('secondary_name', '')
    query_catalog = request.GET.get('catalog', '')
    page_number = request.GET.get('page', '1')

    stocks_queryset = StockMod.objects.select_related('catalog').all()
    if query_secondary:
        stocks_queryset = stocks_queryset.filter(secondary_name__icontains=query_secondary)
    if query_catalog:
        stocks_queryset = stocks_queryset.filter(catalog__primary_name__icontains=query_catalog)

    paginator = Paginator(stocks_queryset, 40)
    try:
        page_number = int(page_number)
    except (TypeError, ValueError):
        page_number = 1
    if page_number < 1:
        page_number = 1

    try:
        stocks = paginator.page(page_number)
    except (PageNotAnInteger, EmptyPage):
        stocks = paginator.page(1)

    return render(request, 'pharma/pages/list.html', {
        'stocks': stocks,
        'query_secondary': query_secondary,
        'query_catalog': query_catalog
    })


def register_view(request):
    if request.method == 'POST':
        form = StockForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Item de estoque registrado com sucesso!')
            return redirect('pharma:list')
        else:
            messages.error(request, 'Erro ao registrar o item. Verifique os dados.')
    else:
        form = StockForm()
    return render(request, 'pharma/pages/register.html', {'form': form, 'is_edit': False})


def stock_edit_view(request, stock_id):
    stock = get_object_or_404(StockMod, id=stock_id)
    if request.method == 'POST':
        form = StockForm(request.POST, instance=stock)
        if form.is_valid():
            form.save()
            messages.success(request, 'Item de estoque atualizado com sucesso!')
            return redirect('pharma:list')
        else:
            messages.error(request, 'Erro ao atualizar o item. Verifique os dados.')
    else:
        form = StockForm(instance=stock)
    return render(request, 'pharma/pages/register.html', {'form': form, 'is_edit': True, 'stock': stock})


def stock_delete_view(request, stock_id):
    stock = get_object_or_404(StockMod, id=stock_id)
    if request.method == 'POST':
        stock.delete()
        messages.success(request, 'Item de estoque excluído com sucesso!')
        return redirect('pharma:list')
    return render(request, 'pharma/pages/confirm_delete.html', {'stock': stock})


@require_http_methods(["GET"])
def catalog_detail(request, catalog_id):
    """API endpoint to get catalog details including presentation"""
    try:
        catalog = CatalogMod.objects.get(id=catalog_id)
        data = {
            'id': catalog.id,
            'primary_name': catalog.primary_name,
            'presentation_id': catalog.presentation.id,
            'presentation_name': str(catalog.presentation),
            'concentration_value': str(catalog.concentration_value) if catalog.concentration_value else '',
            'concentration_unity': catalog.concentration_unity,
            'item_type': catalog.get_item_type_display(),
            'success': True
        }
        return JsonResponse(data)
    except CatalogMod.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Produto não encontrado'}, status=404)


