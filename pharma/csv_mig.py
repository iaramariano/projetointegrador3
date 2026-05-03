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
            try:
                presentation.save()
                print(f"Salvo: {presentation.name}")
            except Exception as e:
                print(f"Erro ao salvar {presentation.name}: {e}")

def exclude_presentations():
    presentations = PharmPresentMod.objects.all()
    presentations.exclude()


def export_catalog():
    path = 'pharma/csv/df_catalog_errors.csv'    
    with open(path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)

        for row in reader:
            presentation = PharmPresentMod.objects.filter(name=row['PRESENTATION'])[0]
            
            errors = []
            
            catalog_item = CatalogMod(
                
                id = row['CATALOG_ID'],
                primary_name = row['PRIMARY_NAME'],
                concentration_value = None,
                concentration_unity = None,
                presentation = presentation,
                assoc_concentration = row['ASSOC_CONC'],
                animal_weight_conc = row['ANIMAL_WEIGHT_CONC'],
                spec_concentration = row['SPEC_CONC'],
                item_type = row['ITEM_TYPE'],
                min_stock = 0
            )
            
            try:
                catalog_item.save()
                print(f"Salvo: {catalog_item.id}")
            except Exception as e:
                print(f"Erro ao salvar item {catalog_item.id}: {e}")
            

def export_stock():
    path = 'pharma/csv/stock_final.csv'    
    with open(path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)

        row_count = 0
        errors = []

        for row in reader:
            catalog_item = CatalogMod.objects.filter(id=row['CATALOG_ID'])[0]
            
            row_count += 1
            
            stock_item = StockMod(
                catalog=catalog_item,
                secondary_name=row['SECONDARY_NAME'],               
                batch_number=row['BATCH_NUMBER'],
            )

            
            if row['EXPIRY'] == 'None' or row['EXPIRY'] == '':
                stock_item.expiry = None
            else:
                stock_item.expiry = row['EXPIRY']

            if row['SKU_QTY'] == 'None' or row['SKU_QTY'] == '':
                stock_item.sku_qty = None
            else:
                stock_item.sku_qty = row['SKU_QTY']
            
            if row['DOSAGE_QTY'] == 'None' or row['DOSAGE_QTY'] == '':
                stock_item.dosage_qty = None
            else:                
                stock_item.dosage_qty = float(row['DOSAGE_QTY'])

            try:
                stock_item.save()
                print(f"Salvo: {row_count}")
            except Exception as e:
                print(f"Erro ao salvar item de estoque {row_count}: {e}")
                errors.append(row_count)

        print(errors)

if __name__ == "__main__":
    export_stock()



