import pandas as pd
from django.core.management.base import BaseCommand
from pets.models import PetsMod

class Command(BaseCommand):
    help = 'Importa pets do CSV'

    def handle(self, *args, **kwargs):
        df = pd.read_csv('pets/pets.csv', encoding='utf-8')

        for _, row in df.iterrows():

            sexo = 'M'
            if str(row['Sexo (Macho/ Fêmea)']).startswith('F'):
                sexo = 'F'

            PetsMod.objects.create(
                name=row['Nome'],
                sex=sexo,
            )

        self.stdout.write(
            self.style.SUCCESS('Pets importados com sucesso!')
        )