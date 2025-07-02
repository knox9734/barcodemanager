# urls.py in products app
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.product_list, name='product_list'),
    path('add/', views.add_product, name='add_product'),
    path('bulk-add/', views.bulk_add_products, name='bulk_add_products'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('product/<int:pk>/delete/', views.product_delete, name='product_delete'),
    path('product/<int:pk>/generate-barcodes/', views.generate_barcodes, name='generate_barcodes'),

]