from django.contrib import admin
from .models import UsersMod
from django.contrib.auth.admin import UserAdmin


# Register your models here.
class UsersAdmin(UserAdmin):
    
    # Lista de campos para exibição na página de listagem de usuários no admin
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'shelter')
    
    
    # Adiciona o campo shelter no campo de edição de usuário no admin
    fieldsets = UserAdmin.fieldsets + (
        ('Instituição', {'fields': ('shelter',)}),
    )

    # Adiciona o campo na página de criação do usuário 
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Instituição', {'fields': ('shelter',)}),
    )

# Agora registramos o modelo USANDO a nossa classe customizada
admin.site.register(UsersMod, UsersAdmin)