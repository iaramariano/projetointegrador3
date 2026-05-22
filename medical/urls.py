from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse

app_name = 'medical'


urlpatterns = [
   
    
    # Página inicial do app medical
    path('', views.medical_home, name='home'),
    
    # Páginas relacionadas ao catálogo de procedimentos
    path('procedure/list/', views.catalog_list, name='catalog_list'),
    path('procedure/register/', views.catalog_register, name='catalog_register'),
    path('procedure/save/', views.catalog_save, name='catalog_save'),
    path('procedure/edit/', views.catalog_edit, name='catalog_edit'),
    path('procedure/delete/', views.catalog_delete, name='catalog_delete'),

    # Páginas relacionadas a eventos médicos

    
    # Variações das páginas (e formulários) para registro de eventos médicos
    path('event/new/', views.event_register, name='event_register'),
    path('event/new/exam/', views.event_register,{'type': 'Exame'}, name='event_register_exam'),
    path('event/new/vaccine/', views.event_register,{'type': 'Vacina'}, name='event_register_vaccine'),
    path('event/new/medication/', views.event_register,{'type': 'Medicação'}, name='event_register_medication'),
    path('event/new/general/', views.event_register,{'type': 'Geral'}, name='event_register_general'),

    # Salva, Edita e exclui registro
    path('event/save/', views.event_save, name='event_save'),
    path('event/edit', views.event_edit, name='event_edit'),
    path('event/delete', views.event_delete, name='event_delete'),

    path('event/history/select', views.event_history_select, name='event_history_select'),
    
    
    # Auxiliares. Filtram pets por critérios para facilitar a seleção
    path('event/pets-by-procedure/', views.pets_by_procedure, name='pets_by_procedure'),
    path('event/pets-by-species/', views.pets_by_species, name='pets_by_species'),

    #path('event/history/', views.event_history, name='event_history'),
]
