from .forms import MedicalEventForm, ExamForm, MedicationForm, VaccineForm
from .models import MedicalEventMod, ExamMod, MedicationMod, VaccineMod

procedure_types = ['Geral', 'Exame', 'Medicação', 'Vacina']

specific_model_procedures = procedure_types[1:]

forms_map = {
        'Exame': ExamForm,
        'Vacina': VaccineForm,
        'Medicação': MedicationForm,
        'Geral': MedicalEventForm
    }

models_map = {
    'Exame': ExamMod,
    'Vacina': VaccineMod,
    'Medicação': MedicationMod,
    'Geral': MedicalEventMod,
}

def pet_age_yrs(pet_age):
    
    if pet_age <=0:
        return "Indefinida"
    
    pet_yrs = pet_age // 12
    pet_months = pet_age % 12
    pet_age = ""

    if pet_yrs > 0:
        pet_age = str(pet_yrs) + ' ano'
        if pet_yrs > 1:
            pet_age += 's'
    
    if pet_months > 0:
        if pet_yrs > 0:
            pet_age += ' e '
        
        pet_age += str(pet_months)
        if pet_months == 1:
            pet_age += ' mês'
        else:
            pet_age += ' meses'

    return pet_age
