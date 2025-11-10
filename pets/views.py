from django.contrib import messages
from django.db.models import Count
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .forms import PetsModForm, SectorModForm, MedicalEventForm, NewStatusForm, MedicalEventSectorForm, SectorSelectForm
from .models import PetsMod, SectorMod, MedicalEventMod

from .services import register_medical_event_pet, register_medical_event_sector

# Classes utilitárias
from .utils import Dates, BgCardColor

from datetime import date


#Instância classes de suporte
dates = Dates() #Classe que possibilita a inclusão dos meses em português para preenchimento dos formulários.
bg_colors = BgCardColor() #Classe que permite a inclusão da cor de fundo do card em cada objeto pet.


# ***********************************************************VIEWS INICIAIS E DE PAINEL DE CONTROLE***********************************************************


def home(request):
    return render(request, 'pets/pages/home.html')

def area_logada(request):
    return redirect ('authors:login')

@login_required(login_url='authors:login', redirect_field_name='next')
def panel(request):
    return render(request, 'pets/pages/panel.html')


# *************************************************************** VIEWS RELACIONADAS A CÃES**********************************************************************

# ***************************************************************************************************************************************************************
 
# View básica de listagem de cães. Reage a diversos cenários: usuário logado ou não, listagem com ou sem parâmetros de busca.
def petlist(request, search=False, filter=False):
    
    context = {'search': search, 'filter': filter}
    
    if request.user.is_authenticated: # Se o usuário estiver logado:

        #Recupera os dados do banco de dados:
        petlist = PetsMod.objects.all().order_by('name') #Seleciona todos os cães cadastrados, ordenados por nome.
        sectors = SectorMod.objects.all() # Seleciona todos os setores cadastrados. (para formulário de busca)
        aptitudes = PetsMod.APTITUDE # Seleciona todas as aptidões possíveis (para formulário de busca)
        
        #Passa os dados login-dependentes para o contexto
        context['sectors'] = sectors
        context['aptitudes'] = aptitudes

    else: #Se o usuário não estiver logado:
        petlist = PetsMod.objects.filter(aptitude='AP').order_by('name') #Seleciona apenas os cães aptos à adoção, ordenados por nome.
    
    
    # Se a página for exibir o resultado de uma busca ou filtragem
    if filter and request.method == 'POST':
        
        allowed_fields = ['name', 'sex', 'sector', 'aptitude'] #Campos permitidos para filtro.

        for key, value in request.POST.items(): #Filtra os dados conforme os parâmetros recebidos.
            if key in allowed_fields:
                if value:
                    if key == 'name':
                        petlist = petlist.filter(name__istartswith=value)
                    else:                
                        petlist = petlist.filter(**{key:value})

    petlist = petlist.exclude(id_pet__isnull=True)   #Limpa a lista de exibição de um possível id nulo.
    
    # Passa os dados não login-dependentes e filtrados (se for o caso) para o contexto
    context['petlist'] = bg_colors.list(petlist) # Adiciona a lista de pets com as cores de fundo ao contexto.
    context['num_results'] = len(petlist)

    # Caso a busca não retorne resultados, exibe uma mensagem adequada.
    if context['num_results'] == 0:
        
        context['search'] = True # Reabre o formulário de busca.
        
        if filter:
            messages.info(request, "Nenhum cão encontrado com os parâmetros informados.")
             
        else:
            messages.info(request, "Nenhum cão cadastrado.")

    return render(request, 'pets/pages/petpage.html', context=context)
# **************************************************************************************************************************************************************

# Gera o formulário de cadastro de cães. Usa o mesmo template da view de edição, mas sem dados preenchidos.
@login_required(login_url='authors:login', redirect_field_name='next')
def pet(request):
           
    form = PetsModForm()
    context = {'form': form, 'months': dates.months, 'years': dates.year_list(), 'pet': pet}
    
    return render(request, 'pets/pages/dog_register.html', context=context)
# **************************************************************************************************************************************************************

# Salva o novo cão no banco de dados e exibe uma mensagem confirmando o cadastro.
@login_required(login_url='authors:login', redirect_field_name='next')
def pet_create(request):

    form = PetsModForm(request.POST, request.FILES)

    
    if request.method == 'POST' and form.is_valid():    
        gender_vowel = 'a' if form.cleaned_data['sex'] == 'F' else 'o'        
        registered_message = form.cleaned_data['name'] + " cadastrad" + gender_vowel + " com sucesso!"
        
        form.save()
        messages.success(request, registered_message)
    
    else:
        messages.error(request, "Algo deu errado! Por favor, repita a operação de cadastro.")

    return redirect('pet:pet')
# **************************************************************************************************************************************************************

# Gera o formulário de cadastro/edição de cães, com os dados do cão selecionado já preenchidos.
@login_required(login_url='authors:login', redirect_field_name='next')
def pet_view(request, id_pet):

    pet = get_object_or_404(PetsMod, id_pet=id_pet)
    form = PetsModForm(instance=pet)
    
    context = {'form': form, 'months': dates.months, 'years': dates.year_list(), 
               'pet': pet, 'bg_color': bg_colors.random()} # Passa a cor de fundo aleatória para o card do pet.

    return render (request, 'pets/pages/dog_register.html', context=context)
# **************************************************************************************************************************************************************

# Salva as alterações feitas no cadastro do cão e exibe uma mensagem confirmando a atualização.
@login_required(login_url='authors:login', redirect_field_name='next')
def pet_update(request, id_pet):
    
    pet = get_object_or_404(PetsMod, id_pet=id_pet)
    form = PetsModForm(request.POST or None, request.FILES or None, instance = pet)

    if request.method == 'POST' and form.is_valid():
        
        gender_vowel = 'a' if form.cleaned_data['sex'] == 'F' else 'o'        
        updated_message = form.cleaned_data['name'] + " atualizad" + gender_vowel + " com sucesso!"
        form.save()
        messages.success(request, updated_message)
    
    else:
        messages.error(request, "Algo deu errado! Por favor, repita a operação de atualização.")
   
    return redirect('pet:pet_view', id_pet=id_pet)
# **************************************************************************************************************************************************************

# Exclui um cão cadastrado do banco de dados.
@login_required(login_url='authors:login', redirect_field_name='next')
def pet_delete(request, id_pet):

    pet = get_object_or_404(PetsMod, id_pet=id_pet)
    
    gender_vowel = 'a' if pet.sex == 'F' else 'o'        
    deleted_message = pet.name + " excluid" + gender_vowel + " com sucesso!"
        
    if request.method == 'POST':
        
        messages.success(request, deleted_message) 
        pet.delete()
    
    else:
        messages.error(request, "Algo deu errado! Por favor, repita a operação de exclusão.")
    
    return redirect('pet:panel')
# ***************************************************************************************************************************************************************


# ***********************************************************VIEWS RELACIONADAS A SETORES************************************************************************


@login_required(login_url='authors:login', redirect_field_name='next')
def sector_manager(request):
          
    form = SectorModForm()
    
    sectors = SectorMod.objects.annotate(resident_number=Count('pets'))
    sector_forms = [ SectorModForm(instance=sector, prefix=str(sector.id_sector)) for sector in sectors ] #Cria uma lista de formulários para a linha retrátil de edição.
    sector_residents = {sector: list(PetsMod.objects.filter(sector=sector.id_sector)) for sector in sectors} #Cria um dicionário com os setores e os pets que estão em cada setor. (P/ FUTURA MELHORIA)
    
    context = {
            'form': form,
            'sectors': sectors,
            'years': dates.year_list(),
            'sector_forms': sector_forms,
            'sector_residents': sector_residents
        }


    return render(request, 'pets/pages/sector_manager.html', context=context)
# ***************************************************************************************************************************************************************

# Cria um novo setor no banco de dados e exibe uma mensagem confirmando a criação.
@login_required(login_url='authors:login', redirect_field_name='next')
def sector_create(request):
       
    form = SectorModForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():    
        
        created_message = form.cleaned_data['name'] + " criado com sucesso!"
        messages.success(request, created_message)
        form.save()
    
    else:
        messages.error(request, "Algo deu errado! Por favor, repita a operação de criação.")
        
    return redirect('pet:sector_manager')
# ***************************************************************************************************************************************************************

# Atualiza os dados do setor selecionado e exibe uma mensagem confirmando a atualização.
@login_required(login_url='authors:login', redirect_field_name='next')    
def sector_update(request, id_sector):
    
    sector = get_object_or_404(SectorMod, id_sector=id_sector)
    form = SectorModForm(request.POST or None, instance = sector)
    
    if request.method == 'POST' and form.is_valid():
        
        updated_message = form.cleaned_data['name'] + " atualizado com sucesso!"
        messages.success(request, updated_message)
        form.save()
    
    else:
         print(form.errors)
         messages.error(request, "Algo deu errado! Por favor, repita a operação de atualização.")
    
    return redirect('pet:sector_manager')
# ***************************************************************************************************************************************************************

# Exclui o setor selecionado do banco de dados.
@login_required(login_url='authors:login', redirect_field_name='next')
def sector_delete(request, id_sector):
    
    sector = get_object_or_404(SectorMod, id_sector=id_sector)
    
    if request.method == 'POST':
        sector.delete()
    
    return redirect('pet:sector_manager')
#****************************************************************************************************************************************************************

# ***********************************************VIEWS RELACIONADAS A EVENTOS MÉDICOS*************

#*****************************************************************************************************************************
# Cria o formulário para registrar um evento médico para um cão específico.

@login_required(login_url='authors:login', redirect_field_name='next')
def dog_medical_event_form(request):

    form = MedicalEventForm()

    new_status = NewStatusForm()

    context = {'form': form, 'new_status': new_status}
    
    return render(request, 'pets/pages/dog_med_event_reg.html', context=context)


#*****************************************************************************************************************************
# Cria o formulário para registrar um evento médico para todos os cães de um setor.

@login_required(login_url='authors:login', redirect_field_name='next')
def sector_medical_event_form(request):

    form = MedicalEventSectorForm()

    sector = SectorSelectForm()

    context = {'form': form, 'sector': sector}
    
    return render(request, 'pets/pages/sector_med_event_reg.html', context=context)
#****************************************************************************************************************************************************************
# Salva o evento médico no banco de dados e exibe uma mensagem confirmando o registro.

@login_required(login_url='authors:login', redirect_field_name='next')
def medical_event_register(request, level=None):

    if level == 'pet': # Salva um evento médico para um cão específico

        if request.method == 'POST':    

            med_event_form = MedicalEventForm(request.POST or None) 
            new_status_form = NewStatusForm(request.POST or None)

            try:          
            
                sucess_message = register_medical_event_pet(med_event_form, new_status_form)
                messages.success(request, sucess_message)
        
            except ValueError as ve:
                messages.error(request, f"Erro: {str(ve)}. Registre o evento médico novamente.")
        
        else:
            messages.error(request, "Ocorreu um erro. Por favor, repita a operação.")
    
        return redirect('pet:dog_medical_event')
    
    elif level == 'sector':  # Salva um evento médico para todos os cães de um setor específico
       

        if request.method == 'POST':
            
            med_event_form = MedicalEventSectorForm(request.POST or None) 
            sector_form = SectorSelectForm(request.POST or None)
        
            try:
                sucess_message = register_medical_event_sector(med_event_form, sector_form)
                messages.success(request, sucess_message)

            except Exception as e:
                messages.error(request, f" Erro: {str(e)}. Por favor, registre o evento médico novamente.")
    
        else:
            messages.error(request, "Ocorreu um erro. Por favor, repita a operação.")
        
        return redirect('pet:sector_medical_event')
    
    else:
        messages.error(request, "Ocorreu um erro. Por favor, repita a operação.")
        return redirect('pet:panel')

#****************************************************************************************************************************************************************
                    

@login_required(login_url='authors:login', redirect_field_name='next')
def dog_med_event_view(request, id_pet):

    pet = get_object_or_404(PetsMod, id_pet=id_pet)
    form = PetsModForm(instance=pet)
    events = (MedicalEventMod.objects
          .filter(patient=pet)
          .order_by('-event_date', '-id_event'))   # ou '-pk'
    
    context = {'form': form, 'months': dates.months, 'years': dates.year_list(), 
               'pet': pet, 'bg_color': bg_colors.random(), # Passa a cor de fundo aleatória para o card do pet.
               'events': events}

    return render (request, 'pets/pages/dog_med_event_view.html', context=context)
    
# ***********************************************************VIEWS RELACIONADAS A USUÁRIOS************************************************************************
@login_required(login_url='authors:login', redirect_field_name='next')
def users(request):
    return render(request, 'pets/pages/users.html')









    


