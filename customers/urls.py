from django.urls import path
from . import views

urlpatterns = [
    path('', views.customer_list_view, name='customer_list'),
    path('<int:customer_id>/', views.customer_detail_view, name='customer_detail'),

    path('customer/<int:customer_id>/delete-product/<int:product_id>/', views.delete_product, name='delete_product'),
    path('customer/<int:customer_id>/delete-server/<int:server_id>/', views.delete_server, name='delete_server'),
    path('customer/<int:customer_id>/delete-contact/<int:contact_id>/', views.delete_contact, name='delete_contact'),
    path('customer/<int:customer_id>/delete-attachment/<int:attachment_id>/', views.delete_attachment, name='delete_attachment'),
    
]
