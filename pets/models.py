from django.db import models
from django.forms import MultiWidget, TextInput
from django.contrib.auth.models import User
from datetime import date, datetime


# Cria o modelo de setor para associar aos pets
class SectorMod(models.Model):
    TYPE = [("I", "Individual"), ("C", "Coletivo")] # Cria as opções de tipo de setor
    id_sector = models.AutoField(primary_key=True)
    name = models.CharField(max_length=65)
    type = models.CharField(max_length=1, choices=TYPE, default="C") # Aplica as opções ao campo

    def __str__(self):
        return f"{self.name}"
            
# Cria o modelo de pets
class PetsMod(models.Model):
        
        #Criando as opções de escolha para a espécie, sexo e  status do animal.
        SPECIES = [("C", "Cão"), ("G", "Gato")]
        STATUS = [("AP", "Apto"), ("IN", "Inapto"), ("PR", "Em preparo"), ("AD", "Adotado"), ("DV", "Devolvido"), ('ES', "Estrelinha")]
        SEXES = [("M", "Macho"), ("F", "Fêmea"), ("I", "Indefinido")]
        ARRIVALS = [('DE', 'Devolução'), ('IN', 'Indefinida'), ('NS', 'Nascimento'), ('RS', 'Resgate'),  ('RC', 'Resgate CED')]
        PLACES = [('IN', 'Indefinido'), ('AB', 'Abrigo'), ('GI', 'Gatil Infantil'), ('GA', 'Gatil Adulto'), ('CI', 'Canil Infantil'), 
                  ('CA', 'Canil Adulto'), ('MI', 'Mirim'), ('LT', 'Lar Temporário'), ('LC', 'Lar Temporário CED'), ('TL', 'Trasladada')]
        
        #Posterior criação de um modelo de PLACEMENTS, nos moldes do de setor do abrigo anterior.
        
        #Campos em si na mesma ordem em que aparecem no formulário.
        
        #Dados básicos do cão
        id_pet = models.BigAutoField(primary_key=True)
        species = models.CharField(max_length=10, choices=SPECIES, default="C")
        name = models.CharField(max_length=100)
        
        sex = models.CharField(max_length=10, choices=SEXES, default="I")
        age = models.SmallIntegerField(blank=True, null=True) # Idade em meses
        arrival = models.CharField(max_length=20, choices=ARRIVALS, default='RS')
        
        arrival_date = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True)
        placement = models.CharField(max_length=20, choices=PLACES, default='AB')
        history = models.TextField(max_length=2000, blank=True, null=True)

        chip = models.CharField(max_length=20, blank=True, null=True, default='Sem Chip')
        status = models.CharField(max_length=20, choices=STATUS, default="PR")
    
        photo = models.ImageField(upload_to='pets/photos/front/%Y/%m/', blank=True, null=True)
        
        #Metadados
        created_at = models.DateTimeField(auto_now_add=True)
        update_at = models.DateTimeField(auto_now=True)
        
        def __str__(self):
            return self.name

# Cria o evento para o cãozinho (paciente) e preenche se cão está apto ou não para adoção
class MedicalEventMod(models.Model):
    
    EVENTS = [('CA', 'Castração'), ('CI', 'Cirurgia'), ('CO', 'Consulta'), ('EX', 'Exame'), 
              ('TR', 'Tratamento'), ('VA', 'Vacinação'), ('OU', 'Outros')]
    
    id_event = models.AutoField(primary_key=True)
    patient = models.ForeignKey(PetsMod, on_delete=models.CASCADE, related_name='medical_events') 
    event = models.CharField(max_length=255, choices=EVENTS, blank=False, null=False, default='CO')
    details = models.CharField(max_length=255, blank=True, null=True)
    event_date = models.DateField(auto_now=False, auto_now_add=False, default=date.today)
    change_status = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.event} registrado para o pet {self.patient} em {self.event_date}"
