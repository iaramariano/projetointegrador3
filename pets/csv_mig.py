import os
import django
import sys
import csv

workdir = os.getcwd()
sys.path.append(workdir)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from pets.models import PetsMod

