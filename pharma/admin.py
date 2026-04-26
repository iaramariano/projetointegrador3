from django.contrib import admin
from .models import PharmGroupMod, PharmPresentMod, CatalogMod, StockMod

class PharmGroupAdmin(admin.ModelAdmin):
    ...
admin.site.register(PharmGroupMod, PharmGroupAdmin)

class PharmPresentAdmin(admin.ModelAdmin):
    ...
admin.site.register(PharmPresentMod, PharmPresentAdmin)

class CatalogAdmin(admin.ModelAdmin):
    ...
admin.site.register(CatalogMod, CatalogAdmin)

class StockAdmin(admin.ModelAdmin):
    ...
admin.site.register(StockMod, StockAdmin)