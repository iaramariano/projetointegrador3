import os
import django
import sys
import csv

workdir = os.getcwd()
sys.path.append(workdir)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from pharma.models import PharmGroupMod

def export_groups():
    path = 'pharma/csv/groups.csv'
    with open(path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # CORREÇÃO: Criar uma instância do modelo
            group = PharmGroupMod(
                name=row['GROUP'],
                allowed_units=row['ALLOWED_UNITS'],
                help_text=row['HELP_TEXT']
            )
            group.save()
            print(f"Salvo: {group.name}")

if __name__ == "__main__":
    export_groups()



