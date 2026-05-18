from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse

app_name = 'medical'


urlpatterns = [
   
    path('', views.medical_home, name='home'), #Página inicial do app medical
    path('list/', views.catalog_list, name='catalog_list'),
    path('register/', views.catalog_register, name='catalog_register'),
    path('edit_procedure/<int:procedure_id>', views.catalog_register, name='catalog_edit')
    #path('api/catalog/<int:catalog_id>/', views.catalog_detail, name='catalog_detail'),
]
