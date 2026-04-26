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
    
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=30, blank=False, null=False, unique=True)
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
    
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=30, blank=False, null=False, unique=True)
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
    

class CatalogMod(AuditMixin):

    # Modelo que registra os itens de catálogo disponíveis para registro e controle de estoque

    ITEM_TYPES = [('MED', 'Medicamento'), ('SUP', 'Suplemento'), ('INS', 'Insumo'), ('DIS', 'Dispositivo'), ('COS', 'Cosmético')]
    
    id = models.BigAutoField(primary_key=True)
    primary_name = models.CharField(max_length=100, blank=False, null=True)
    concentration_value = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True)
    concentration_unity = models.CharField(max_length=10, blank=False, null=False)
    presentation = models.ForeignKey(PharmPresentMod, on_delete=models.PROTECT, null=False, blank=False)

    # Quando o medicamento é uma associação e a concentração é especificada em spec_concentration como 
    # uma lista de dicionários {drug, concentration, unity}
    assoc_concentration = models.BooleanField(default=False)
    
    # A dosagem é vinculada ao peso do animal. Expresso também em spec_concentration
    animal_weight_conc = models.BooleanField(default=False)

    spec_concentration = models.JSONField(blank=True, null=True)
    item_type = models.CharField(max_length=10, choices=ITEM_TYPES, default='MED')
    
    # Campo para alertas de compra para medicamento 
    min_stock = models.IntegerField(default=0)
    
    class Meta:
        
        verbose_name = "Definição de produto"
        verbose_name_plural = "Catálogo de Produtos"

        constraints = [models.UniqueConstraint(
            fields=['primary_name', 'concentration_value', 'concentration_unity', 'presentation'],
            name='unique_catalog_item')]
    
    def __str__(self):
        return f"{self.primary_name} {self.concentration_value or ''}{self.concentration_unit or ''} ({self.presentation} {self.spec_concentration})"
    
class StockMod(AuditMixin):

    # Modelo que registra os itens de estoque

    id = models.BigAutoField(primary_key=True)
    catalog = models.ForeignKey(CatalogMod, on_delete=models.PROTECT, related_name='stocks')
    secondary_name = models.CharField(max_length=100, blank=True, null=True)
    batch_number = models.CharField(max_length=100, null=True, blank=True)
    stocking_unity = models.CharField(max_length=100, null=True, blank=True)
    expiry = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True)
    sku_qty = models.IntegerField(null=False, blank=False, default=1)
    dosage_qty = models.DecimalField(decimal_places=2, max_digits=5, blank=True, null=True)