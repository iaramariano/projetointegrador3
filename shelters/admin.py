from django.contrib import admin
from .models import SheltersMod

# Register your models here.
class SheltersAdmin(admin.ModelAdmin):
    ...

admin.site.register(SheltersMod, SheltersAdmin)