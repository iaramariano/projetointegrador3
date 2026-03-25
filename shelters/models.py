from django.db import models

# Create your models here.

class SheltersMod(models.Model):

    id_shelter = models.AutoField(primary_key=True, db_column='id_shelter')
    name = models.CharField(max_length=100, db_column='name', blank=False, null=False)
    options = models.JSONField(default=dict, db_column='options', blank=True, null=True)

    def __str__(self):
        return f"{self.name}"