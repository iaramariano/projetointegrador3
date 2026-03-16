from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = "pet"

urlpatterns = [
    path('', views.home, name='home'),
    path('panel', views.panel, name='panel'), #teste da nova página
    path('users', views.users, name='users'),
    
    # Pet URLs
    
    path('pet', views.pet, name='pet'),
    path('pet/create', views.pet_create, name='pet_create'),
    path('pet/view/<int:id_pet>', views.pet_view, name='pet_view'),
    path('pet/update/<int:id_pet>', views.pet_update, name='pet_update'),
    path('pet/delete/<int:id_pet>', views.pet_delete, name='pet_delete'),
    
    path('petlist', views.petlist, name='petlist'),
    
    ## Sector URLs
    path('sector', views.sector_manager, name='sector_manager'),
    path('sector/create', views.sector_create, name='sector_create'),
    path('sector/update/<int:idsetor>', views.sector_update, name='sector_update'),
    path('sector/delete/<int:idsetor>', views.sector_delete, name='sector_delete'),

    #Search URLs
    path('search', views.petlist, {'search': True}, name='search'),
    path('search_respost', views.petlist,{'filter': True}, name='search_respost'),

    #Medical Event URLs
    path('dog_medical_event', views.dog_medical_event_form, name='dog_medical_event'),
    path('sector_medical_event', views.sector_medical_event_form, name='sector_medical_event'),
    path('dog_event/register', views.medical_event_register, {'level': 'pet'}, name='dog_event_register'),
    path('sector_event/register', views.medical_event_register, {'level': 'sector'}, name='sector_event_register'),
    path('pet/dog_med_event_view/<int:id_pet>', views.dog_med_event_view, name='dog_med_event_view'),
    ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
