from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse

app_name = 'pharma'


urlpatterns = [
    path('list/', views.list_view, name='list'),
    path('', views.pharmagen, name='about'),
    path('register/', views.register_view, name='register'),
    path('stock/<int:stock_id>/edit/', views.stock_edit_view, name='stock_edit'),
    path('stock/<int:stock_id>/delete/', views.stock_delete_view, name='stock_delete'),
    path('api/catalog/<int:catalog_id>/', views.catalog_detail, name='catalog_detail'),
]
