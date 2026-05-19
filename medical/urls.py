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

    path('event/new/', views.event_type_select, name='event_type_select'),
    path('event/new/exam/', views.event_new_exam, name='event_new_exam')
]
