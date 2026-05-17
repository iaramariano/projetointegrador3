from django.shortcuts import render, redirect
from .models import ProcedCatalogMod
from django.contrib.auth.decorators import login_required
from .forms import CatalogForm

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

    form = CatalogForm()

    context = {
        'form': form
    }

    return render(request, 'medical/pages/catalog_register.html', context=context)




