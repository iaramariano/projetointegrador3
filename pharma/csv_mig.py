import os
import django
import sys
import csv

workdir = os.getcwd()
sys.path.append(workdir)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from pharma.models import PharmGroupMod, PharmPresentMod, CatalogMod, StockMod

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


def export_presentations():
    path = 'pharma/csv/Presentations.csv'    
    with open(path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)

        for row in reader:
            logical_group = PharmGroupMod.objects.filter(name=row['LOGICAL_GROUP'])[0]
            
            presentation = PharmPresentMod(
                name = row['PRESENTATION'],
                group = logical_group,
                dispensing_unit = row['DISPENSING_UNIT'],
                control_type = row['CONTROL_TYPE']
            )
            presentation.save()
            print(f"Salvo: {presentation.name}")
    
def exclude_presentations():
    presentations = PharmPresentMod.objects.all()
    presentations.exclude()

def export_catalog():
    ...

# tratar a data de expiry antes de subir

def export_stock():
    ...


if __name__ == "__main__":
    export_presentations()



