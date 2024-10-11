from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tickets/', include('tickets.urls')), 
    path('users/', include('users.urls')), 
    path('reports/', include('reports.urls')), 
    path('products/', include('products.urls')),  
    path('customers/', include('customers.urls')),  
    
    
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
