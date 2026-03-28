import os
import uuid
from django.db import models
from django.utils.text import slugify

# Função de apoio para gerar um nome de arquivo único para as imagens de logo
def shelter_logo_upload_to(instance, filename):
    # Pega a extensão do arquivo
    ext = filename.split('.')[-1]
    # Pega o nome do abrigo e cria um slug para ele, ou usa um nome genérico se não houver nome
    shelter_name = slugify(instance.name or f"shelter_{instance.id}")

    # Gera um nome de arquivo único usando UUID
    unique_name = f"{shelter_name}_{uuid.uuid4().hex[:8]}"
    new_filename = f"{unique_name}.{ext}"
    upload_to = 'shelters/img/logos'

    return os.path.join(upload_to, new_filename)

# Create your models here.

class SheltersMod(models.Model):

    id_shelter = models.AutoField(primary_key=True, db_column='id_shelter')
    name = models.CharField(max_length=100, db_column='name', blank=False, null=False)
    logo = models.ImageField(upload_to=shelter_logo_upload_to, db_column='logo', blank=True, null=True)
    options = models.JSONField(default=dict, db_column='options', blank=True, null=True)

    def __str__(self):
        return f"{self.name}"