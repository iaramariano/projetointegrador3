from django.db import models


# Create your models here.

class AuditMixin(models.Model):
    # Modelo com campos de auditoria para adicionar a todos os modelos
    
    # Registros de horário e data
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Registros de usuário
    created_by = models.ForeignKey('users.UsersMod', on_delete=models.SET_NULL, null=True, blank=True, related_name='%(app_label)s_%(class)s_created', 
                                   editable=False)
    updated_by = models.ForeignKey('users.UsersMod', on_delete=models.SET_NULL, null=True, blank=True, related_name='%(app_label)s_%(class)s_updated',
                                   editable=False)
    
    class Meta:
        abstract = True


class PharmGroupMod(AuditMixin):

    # Modelo que contém os grupos de apresentações farmacêuticas e delimita as unidades de Concentrações disponíveis para seleção
    
    id_group = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30, blank=False, null=False)
    allowed_units = models.JSONField(default=list, blank=True, null=True)
    help_text = models.CharField(max_length=300, blank=True, null=True)

    # Metadados
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey('users.Usersmod', on_delete=models.SET_NULL, null=True, blank=True, related_name='%(class)s_created')
    updated_by = models.ForeignKey('users.Usersmod', on_delete=models.SET_NULL, null=True, blank=True, related_name='%(class)s_updated')

    def __str__(self):
        return f"{self.name} : {self.help_text}"
    

class PharmPresentMod(AuditMixin):

    # Modelo que contém as apresentações farmacêuticas. Armazena as unidades de uso e tipo de controle

    CONTROL_TYPES = [('NUM', 'Numérico'), ('NIV', 'Nível'), ('USO', 'Uso')]
    
    id_presentation = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30, blank=False, null=False)
    group = models.ForeignKey(PharmGroupMod, on_delete=models.SET_DEFAULT, null=False, blank=False, default='LIQUIDO')
    dispensing_unit = models.CharField(max_length=20, blank=False, null=False)
    control_type = models.CharField(max_length=10, choices=CONTROL_TYPES, null=False, blank=False, default='NIV')

     # Metadados
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey('users.Usersmod', on_delete=models.SET_NULL, null=True, blank=True, related_name='%(class)s_created')
    updated_by = models.ForeignKey('users.Usersmod', on_delete=models.SET_NULL, null=True, blank=True, related_name='%(class)s_updated')

    def __str__(self):
        return self.name
    

class CatalogItemMod(AuditMixin):

    # Modelo que registra os itens de catálogo disponíveis para registro e controle de estoque

    ITEM_TYPES = [('MED', 'Medicamento'), ('SUP', 'Suplemento'), ('INS', 'Insumo'), ('DIS', 'Dispositivo'), ('COS', 'Cosmético')]
    
    id_catalog_item = models.AutoField(primary_key=True)
    primary_name = models.CharField(max_length=100, blank=False, null=True)
    concentration_value = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True)
    concentration_unity = models.CharField(max_length=10, blank=False, null=False)
    presentation = models.ForeignKey(PharmPresentMod, on_delete=models.SET_DEFAULT, default='Solução', null=False, blank=False)

    assoc_concentration = models.BooleanField(default=False)
    animal_weight_conc = models.BooleanField(default=False)

    spec_concentration = models.JSONField(default=list, blank=True, null=True)
    item_type = models.CharField(max_length=10, choices=ITEM_TYPES, default='MED')
    
    class Meta:
        
        verbose_name = "Definição de produto"
        verbose_name_plural = "Catálogo de Produtos"

        constraints = [models.UniqueConstraint(
            fields=['primary_name', 'concentration_value', 'concentration_unity', 'presentation', 'spec_concentration'],
            name='unique_catalog_item')]
    
    def __str__(self):
        return f"{self.primary_name} {self.concentration_value or ''}{self.concentration_unit or ''} ({self.presentation} {self.spec_concentration})"