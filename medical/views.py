from django.shortcuts import render, redirect, get_object_or_404
from .models import ProcedCatalogMod
from django.contrib.auth.decorators import login_required
from .forms import CatalogForm
from django.contrib import messages

# Create your views here.

@login_required(login_url='users:login', redirect_field_name='next')
def medical_home(request):
    return render(request, 'medical/pages/medical_home.html')

#********************************************************************************************
#*******VIEWS RELACIONADAS AO CATALOGO DE PROCEDIMENTOS REALIZADOS PELO ABRIGO#**************
#********************************************************************************************

# View de lista de Procedimentos registrados no Catálogo
@login_required(login_url='users:login', redirect_field_name='next')
def catalog_list(request):
    
    procedures = ProcedCatalogMod.objects.all().order_by('name')

    alternative_list = []
    
    for procedure in procedures:
        alternative_string = ''
        if procedure.alternatives:
            for alternative in procedure.alternatives:
                if len(alternative_string) > 0:
                    alternative_string += ", "

                proced_alt = ProcedCatalogMod.objects.filter(id=alternative).first()
                alternative_string += proced_alt.name

        alternative_list.append(alternative_string)

    procedures_to_send = zip(procedures, alternative_list)
    
    n_procedures = len(procedures)

    context = {
        'procedures': procedures_to_send,
        'n_procedures': n_procedures,
    }
    
    return render(request, 'medical/pages/catalog_list.html', context=context)
#******************************************************************************************

# Cria o formulário para editar/adicionar um novo procedimento ao catálogo

def catalog_register(request):

    if request.method == 'POST':    
        
        
        
        # Verifica se se trata de uma edição de procedimento
        procedure_id = request.POST.get('procedure_id')

        if procedure_id:

            procedure_to_edit = get_object_or_404(ProcedCatalogMod, id=procedure_id)
            form = CatalogForm(instance=procedure_to_edit)

            context['form'] = form
            return render(request, 'medical/pages/catalog_register.html', context=context)

        form = CatalogForm(request.POST)
        
        if form.is_valid():
            
            chosen_species = form.cleaned_data['species']
            
            min_application_value = form.cleaned_data['min_application']

            if not min_application_value:
                min_application_value = 1
            
            if chosen_species == 'Todas':
                
                species_pl = ['Cão', 'Gato']

                for species_name in species_pl:
                    proced_spec = ProcedCatalogMod(
                        name = form.cleaned_data['name'],
                        type = form.cleaned_data['type'],
                        species = species_name,
                        min_application =  min_application_value,
                        min_interval = form.cleaned_data['min_interval'],
                        repetition = form.cleaned_data['repetition'],
                        mandatory = form.cleaned_data['mandatory'],
                        alternatives = form.cleaned_data['alternatives'],
                        description = form.cleaned_data['description']
                        )
                    
                    proced_spec.save()
            else:
                procedure = form.save(commit=False)
                procedure.species = chosen_species
                procedure.min_application = min_application_value
                procedure.save()
            
            messages.success(request, 'Procedimento registrado com sucesso!')
            return redirect('medical:catalog_list')
        
        else:
            print(form.errors)
            messages.error(request, 'Erro ao registrar o procedimento. Verifique os dados.')
            return redirect('medical:catalog_register')
    else:
        
        form = CatalogForm()
        context = {
            'form': form
        }
        return render(request, 'medical/pages/catalog_register.html', context=context)