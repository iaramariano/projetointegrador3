from django.http import Http404, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib import messages
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from .forms import CatalogForm, StockForm
from .models import CatalogMod

def pharmagen(request):
    return render(request, 'pharma/pages/pharmagen.html')

def list_view(request):
    return render(request, 'pharma/pages/list.html')


def register_view(request):
    if request.method == 'POST':
        form = StockForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Item de estoque registrado com sucesso!')
            return redirect('pharma:list')  # Assuming there's a list view
        else:
            messages.error(request, 'Erro ao registrar o item. Verifique os dados.')
    else:
        form = StockForm()
    return render(request, 'pharma/pages/register.html', {'form': form})


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


