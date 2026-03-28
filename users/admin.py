from django.contrib import admin
from .models import UsersMod


# Register your models here.
class UsersAdmin(admin.ModelAdmin):
    ...
admin.site.register(UsersMod, UsersAdmin)