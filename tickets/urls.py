from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.ticket_create_view, name='ticket_create'),
    path('<int:pk>/', views.ticket_detail, name='ticket_detail'),
    path('search/', views.ticket_search, name='ticket_search'),
    path('search/<int:pk>/', views.ticket_search_detail, name='ticket_search_detail'),
    path('my-tickets/', views.my_tickets, name='my_tickets'),
    path('all/', views.all_tickets, name='all_tickets'),
    path('<int:pk>/confirm-delete/', views.ticket_confirm_delete_view, name='ticket_confirm_delete'),
    path('assign/', views.assign_tickets_view, name='assign_tickets'),

    path('get-customer-products/', views.get_customer_products, name='get_customer_products'),

    
]
