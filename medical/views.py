
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from .forms import CatalogForm, MedicationForm, ExamForm, VaccineForm, MedicalEventForm
from .models import ProcedCatalogMod, MedicalEventMod, ExamMod, VaccineMod, MedicationMod
from .utils import procedure_types, forms_map, specific_model_procedures, models_map, pet_age_yrs

from pets.models import PetsMod
from pets.forms import PetsModForm

import json

# Create your views here.


# View inicial do módulo médico
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

# Cria o formulário de registro de procedimento no catálogo
def catalog_register(request):

    form = CatalogForm()
    
    context = {
            'form': form
    }
        
    return render(request, 'medical/pages/catalog_register.html', context=context)

# Salva um novo procedimento ou a edição de um procedimento já registrado

def catalog_save(request):
    
    if request.method == 'POST':

        # Verifica se se trata de uma edicção
        procedure_id = request.POST.get('procedure_id')

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
# Gera o formulário de edição de procedimentos em catálogo

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
# Exclui um procedimento do catálogo

def catalog_delete(request):

    if request.method == 'POST':

        procedure_id = request.POST.get('procedure_id')
        procedure = get_object_or_404(ProcedCatalogMod, id=procedure_id)

        if procedure:
            procedure.delete()
        
        return redirect('medical:catalog_list')
    
    return redirect('medical:catalog_list')

#********************************************************************************************
#*******VIEWS RELACIONADAS AO REGISTRO DE PROCEDIMENTOS PARA OS PETS*********8#**************
#********************************************************************************************

#****************VIEW DE PREPARAÇÃO DO FORMULÁRIO DE NOVOS EVENTOS*************************

def event_register(request, type):
    
    if not type or type not in procedure_types:
        messages.error(request, "Ocorreu uma falha inesperada. Selecione novamente o tipo de evento médico a ser registrado.")
        return redirect('medical:home')

    form_class = forms_map.get(type)

    form = form_class()

    if type == 'Geral':
        form.fields['procedure'].queryset = ProcedCatalogMod.objects.exclude(type__in=specific_model_procedures).order_by('name')
    else:
        form.fields['procedure'].queryset = ProcedCatalogMod.objects.filter(type=type).order_by('name')

    context = {
        'form': form,
        'type': type
    }

    return render(request, 'medical/pages/event_register.html', context=context)
        
#***********************************************************************************************
# Salva novos eventos e alterações em eventos já salvos

def event_save(request):
    
    type = request.POST.get('type')
    event_id = request.POST.get('event_id')

    if not type or type not in procedure_types:
        messages.error(request, "Ocorreu uma falha inesperada. Selecione novamente o tipo de evento médico a ser registrado.")
        return redirect('medical:home')

    if type not in specific_model_procedures:
        type = 'Geral'


    if request.method == 'POST':
            
        form_class = forms_map[type]
        model_class = models_map[type]
        
        event = get_object_or_404(model_class, id=event_id) if event_id else None
        form = form_class(request.POST, request.FILES, instance=event)

        if form.is_valid():
            
            event = form.save()
            pet = event.pet
                
            if event_id:
                messages.success(request, f"{event} editado com sucesso")
                
            else:
                messages.success(request, f"{event} registrado com sucesso")
        
            
            events = MedicalEventMod.objects.select_related('pet', 'procedure').select_subclasses().filter(pet=pet)

            pet_age_str = pet_age_yrs(pet.age)
            
            context = {
                'events': events,
                'pet': pet,
                'pet_age_str': pet_age_str,
                'n_events': events.count()
            }
            
            return render(request, 'medical/pages/event_history.html', context=context)
    
    else:
        messages.error(request, "Ocorreu um erro inesperado. Realize a operação novamente.")
        return redirect('medical:home')
#***********************************************************************************************
def event_edit(request):

    if request.method == 'POST':

        type = request.POST.get('event_type')
        event_id = request.POST.get('event_id')

        if not type or not event_id or type not in procedure_types:
            messages.error(request, "Ocorreu um erro inesperado. Realize a operação novamente.")
            return redirect('medical:home')
        
        if type not in specific_model_procedures:
            type = 'Geral'

        form_class = forms_map.get(type)
        model_class = models_map.get(type)
        
        event = get_object_or_404(model_class, id=event_id)

        form = form_class(instance=event)

    if type == 'Geral':
        form.fields['procedure'].queryset = ProcedCatalogMod.objects.exclude(type__in=specific_model_procedures).order_by('name')
    else:
        form.fields['procedure'].queryset = ProcedCatalogMod.objects.filter(type=type).order_by('name')
    
    
    context = {
        'form': form,
        'type': type
    }

    return render(request, 'medical/pages/event_register.html', context=context)

#***********************************************************************************************
def event_delete(request):

    event_id = request.POST.get('event_id')
    type = request.POST.get('type')
    
    if request.method != 'POST' or not event_id or not type:
        messages.error(request, "Ocorreu um erro inesperado. Realize a operação novamente.")
        return redirect('medical:home')
    
    if type not in specific_model_procedures:
        type = 'Geral'

    model_class = models_map.get(type)

    event = get_object_or_404(model_class, id=event_id)
    pet = event.pet
    
    messages.success(request, f"{event} excluído com sucesso!")
    
    event.delete()

    events = MedicalEventMod.objects.select_related('pet', 'procedure').select_subclasses().filter(pet=pet)

    pet_age_str = pet_age_yrs(pet.age)


    context = {
        'events': events,
        'pet': pet,
        'pet_age_str': pet_age_str,
        'n_events': events.count()
    }

    return render (request, 'medical/pages/event_history.html', context=context)

#***********************************************************************************************
def event_history_select(request):

    pet_id = request.POST.get('id_pet') or request.GET.get('id_pet')
    
    if pet_id:
        
        pet = get_object_or_404(PetsMod, id_pet=pet_id)
        events = MedicalEventMod.objects.select_related('pet', 'procedure').select_subclasses().filter(pet=pet)

        pet_age_str = pet_age_yrs(pet.age)

        context = {
            'events': events,
            'pet': pet,
            'pet_age_str': pet_age_str,
            'n_events': events.count()
        }
        
        return render(request, 'medical/pages/event_history.html', context=context)    
    
    if request.method == 'GET':
        return render(request, 'medical/pages/history_select.html')
        
    messages.error(request, "Ocorreu um erro inesperado. Realize a operação novamente.")
    return redirect('medical:home')

#***********************************************************************************************

# Filtra os pets por procedimento. Auxiliar na página de registro de eventos médicos.
def pets_by_procedure(request):
    
    procedure_id = request.GET.get('procedure_id')
    procedure = get_object_or_404(ProcedCatalogMod, id=procedure_id)
    
    pets = PetsMod.objects.filter(species=procedure.species)
    data = [{'id': pet.id_pet, 'name': pet.name} for pet in pets]
    
    return JsonResponse(data, safe=False)
#***********************************************************************************************
# Filtra os pets por espécie. Auxiliar na página de seleção de histórico médico.

def pets_by_species (request):

    species = request.GET.get('species')
    
    pets = PetsMod.objects.filter(species=species)
    data = [{'id': pet.id_pet, 'name': pet.name} for pet in pets]

    return JsonResponse(data, safe=False)
