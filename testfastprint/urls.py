from django.urls import path
from . import views

urlpatterns = [
    path('', views.produk, name='produk'),
    path('add/', views.add_produk, name='add_produk'),
    path('edit/<int:id>/', views.edit_produk, name='edit_produk'),
    path('delete/<int:id>', views.delete_produk, name='delete_produk'),
    path('sync-data/', views.sync_data_view, name='sync_data'),

    #api version
    path('api/', views.product_list, name='product_list'),
    path('api/add/', views.product_create, name='product_create'),
    path('api/edit/<int:id>/', views.product_update, name='product_edit'),
    path('api/delete/<int:id>/', views.product_delete, name='product_delete'),
]