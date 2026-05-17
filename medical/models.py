from django.db import models
from pets.models import PetsMod
from pharma.models import CatalogMod
from model_utils.managers import InheritanceManager


#Modelo de procedimentos médicos disponíveis/oferecidos pelo abrigo

class ProcedCatalogMod(models.Model):
    TYPE_CHOICES = [
        ('CIRUGIA', 'Cirurgia'),
        ('EXAME', 'Exame'),
        ('MEDICAÇÃO', 'Medicação'),
        ('TERAPIA', 'Terapia'),
        ('VACINA', 'Vacina')
    ]

    SPECIES_CHOICES = [('GATO', 'Gato'), ('CÃO', 'Cão')]
    
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100, blank=False, null=False)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    species = models.CharField(max_length=10, choices=SPECIES_CHOICES)
    min_application = models.IntegerField(default=1)
    min_interval = models.IntegerField(blank=True, null=True)
    repetition = models.IntegerField(blank=True, null=True)
    mandatory = models.BooleanField(default=False)
    alternatives = models.JSONField(default=list, blank=True, null=True)
    description = models.TextField(blank=True)
                                   
    def __str__(self):
        return f"{self.name} ({self.get_tipo_display()}): {self.description}"

    class Meta:
        verbose_name = "Catálogo de Procedimento"
        verbose_name_plural = "Catálogo de Procedimentos"

        constraints = [models.UniqueConstraint(
            fields=['name', 'type', 'species'],
            name='unique_catalog_procedure')]
    

# Modelo de eventos médicos

class MedicalEventMod(models.Model):

    id = models.BigAutoField(primary_key=True)
    pet = models.ForeignKey(PetsMod, on_delete=models.CASCADE, related_name='eventos_medicos')
    procedure = models.ForeignKey(ProcedCatalogMod, on_delete=models.CASCADE, related_name='procedimentos_realizados')

    date = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True)
    healthcare_provider = models.CharField(max_length=100, blank=True, null=True) #Possibilidade de cadastrar cuidadores/veterinários mais pra frente ou até cruzar com usuários
    outcome = models.CharField(max_length=100, blank=True, null=True)
    
    change_status = models.BooleanField(default=False, blank=True)
    notes = models.TextField(blank=True)

    # Metadados de Criação (No futuro, expandir com os métodos de auditoria de usuário usados em Pharma)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Integra com os subeventos médicos (exame, vacina, tratamento, etc)
    objects = InheritanceManager()

    class Meta:
        ordering = ['-date']

        verbose_name = "Registro de Eventos Médicos"


# Expansão do modelo de eventos médicos para adicionar campos específicos de exame. Posteriormente, adicionar a possibilidade de subir um laudo (report) em pdf

class ExamMod(MedicalEventMod):
    positive = models.BooleanField(default=False)
    report = models.TextField(blank=True)

    class Meta:
        verbose_name = "Registro de Exames"


# Expansão do modelo de eventos médicos para adicionar campos específicos de vacina. Posteriormente, adicionar alertas de próxima dose.
class VaccineMod(MedicalEventMod):
    batch = models.CharField(max_length=50, blank=True)
    next_dose = models.DateField(auto_now=False, auto_now_add=False, blank=True)


# Expansão do modelo de eventos médicos para adicionar receitas ou aplicações de medicações. Posteriormente, implantar alertas 
# e adequar a frequência para entender por dia, por semana, por mês, etc.

class MedicationMod(MedicalEventMod):
    medicine = models.ForeignKey(CatalogMod, on_delete=models.PROTECT)
    dosage = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True)
    frequency = models.PositiveIntegerField(null=True, blank=True)
    duration = models.PositiveIntegerField(null=True, blank=True)