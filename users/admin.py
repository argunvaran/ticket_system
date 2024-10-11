from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'is_manager']  # is_manager gösterilecek
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('is_manager',)}),  # is_manager alanını admin paneline ekledik
    )

admin.site.register(CustomUser, CustomUserAdmin)
