from django.db import models
from django.contrib.auth.models import AbstractUser


class UsersMod(AbstractUser):
    # Metadados
    shelter = models.ForeignKey('shelters.SheltersMod', on_delete=models.SET_NULL, null=True, blank=True, 
                                related_name='users')
    created_at = models.DateTimeField(auto_now_add=True, db_column='created_at')
    update_at = models.DateTimeField(auto_now=True, db_column='update_at')

