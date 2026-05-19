from django.shortcuts import render, redirect, get_object_or_404
from .models import ProcedCatalogMod
from django.contrib.auth.decorators import login_required
from .forms import CatalogForm
from django.contrib import messages
import json

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
        
            alternatives = procedure.alternatives
        
            if isinstance(alternatives, str):
                alternatives = json.loads(alternatives)
        
            for alternative_id in alternatives:
            
                if len(alternative_string) > 0:
                    alternative_string += ", "
            
                proced_alt = ProcedCatalogMod.objects.filter(id=alternative_id).first()
            
                if proced_alt:
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

# Cria o formulário de registro de procedimento para catálogo

def catalog_register(request):

    form = CatalogForm()
    
    context = {
            'form': form
    }
        
    return render(request, 'medical/pages/catalog_register.html', context=context)

def catalog_save(request):
    
    if request.method == 'POST':

        # Verifica se se trata de uma edicção
        procedure_id = request.POST.get('procedure_id')
        print(procedure_id)

        if procedure_id:
            
            procedure = get_object_or_404(ProcedCatalogMod, id=procedure_id)
            form = CatalogForm(request.POST, instance=procedure)

            if form.is_valid():    
                form.save()

            return redirect('medical:catalog_list')
            
        # Adição de um novo procedimento       
        else:

            form = CatalogForm(request.POST)
        
            if form.is_valid():
            
                chosen_species = form.cleaned_data['species']    
                min_application_value = form.cleaned_data['min_application']

                # Garantir o valor mínimo de 1 aplicação
                if not min_application_value:
                    min_application_value = 1
            
                
                # Caso um procedimento seja válido para as duas espécies, salva dois procedimentos uma para cada para gerar 2 ids.
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
                messages.error(request, 'Erro ao registrar o procedimento. Verifique os dados.')
                return redirect('medical:catalog_register')
        
    return redirect('medical:catalog_register')

#******************************************************************************************
# Captura a instância e envia o formulário povoado para a edição de um procedimento

def catalog_edit(request):
     
    if request.method == 'POST':
        
        procedure_id = request.POST.get('procedure_id')
        procedure = get_object_or_404(ProcedCatalogMod, id=procedure_id)
        
        form = CatalogForm(instance=procedure)

        context = {
            'form': form,
            'procedure': procedure
        }
        
        return render(request, 'medical/pages/catalog_register.html', context=context)
    
    return redirect('medical:catalog_list')

#******************************************************************************************
# Exclui o procedimento de catálogo selecionado

def catalog_delete(request):

    if request.method == 'POST':

        procedure_id = request.POST.get('procedure_id')
        procedure = get_object_or_404(ProcedCatalogMod, id=procedure_id)

        if procedure:
            procedure.delete()
        
        return redirect('medical:catalog_list')
    
    return redirect('medical:catalog_list')