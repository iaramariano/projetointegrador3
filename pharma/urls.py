from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse

app_name = 'pharma'


urlpatterns = [
   
    path('test/', views.test_view, name='test'   ),
    path('', views.pharmagen, name='about'),
]
