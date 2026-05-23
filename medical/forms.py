from django import forms
from .models import ProcedCatalogMod, MedicalEventMod, VaccineMod, ExamMod, MedicationMod

# Formulário para cadastro de procedimentos
#Futuramente, incluir mensagens de erro para cada campo, e validações específicas 
# (ex: se o procedimento for obrigatório, os campos de número mínimo de aplicações e intervalo máximo entre as aplicações mínimas devem ser preenchidos)
class CatalogForm(forms.ModelForm):
    
    
    species_choices = ProcedCatalogMod.SPECIES_CHOICES
    species_choices.append(('Todas', 'Todas'))
    
    
    name = forms.CharField(
        label='Nome do procedimento',
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome do procedimento'})
        )
    
    type = forms.ChoiceField(
        label='Tipo de procedimento',
        required=True,
        choices=ProcedCatalogMod.TYPE_CHOICES,
        initial='CONSULTA',
        widget=forms.Select(attrs={'class': 'form-select'})
        )

    species= forms.ChoiceField(
        label='Espécie as quais o procedimento se aplica',
        required=True,
        choices=species_choices,
        initial='CÃO',
        widget= forms.Select(attrs={'class': 'form-select'})
    )

    mandatory = forms.BooleanField(
         label='Procedimento obrigatório para adoção',
         required=False, 
         initial=False, 
         widget= forms.CheckboxInput(attrs={'class': 'form-check-input', 'onchange':'mandatorySection();'})
    )

    min_application = forms.IntegerField(
        label='Número mínimo de aplicações do procedimento',
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

    min_interval = forms.IntegerField(
        label='Intervalo máximo (em dias) entre as aplicações mínimas do procedimento',
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

    repetition = forms.IntegerField(
        label='Intervalo (em dias) para a próxima aplicação / reforço do procedimento',
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

    alternatives = forms.CharField(
         label = 'Quais outros procedimentos podem substituí-lo?',
         required = False,
         widget = forms.TextInput(attrs={'class': 'form-control', 'rows': 2})
    )

    description = forms.CharField(
        label='Descrição',
        required=False,
        widget = forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder':'Breve descrição do procedimento'})
    )
    
    class Meta:
        model = ProcedCatalogMod
        fields = ['name', 'type', 'min_application', 'min_interval', 'repetition', 'mandatory', 'alternatives', 'description']
        
    def __init__(self, *args, **kwargs):
        
        super().__init__(*args, **kwargs)
        
    def clean_name(self):
        name = self.cleaned_data.get('name', '')
        return name.capitalize()
    
    def clean_species(self):
        species = self.data.get('species')
        
        if species == 'Todas':
            return 'Todas'
        
        return self.fields['species'].clean(species)
    
    #************************************************************************************************************************************

    # Expandir o formulário para incluir também eventos como Nascimento, Falecimento, Doenças Diagnosticadas (para compor um histórico médico mais completo)
    
class MedicalEventForm(forms.ModelForm):
    class Meta:
        model = MedicalEventMod
        fields = ['pet', 'procedure', 'date', 'healthcare_provider', 'outcome', 'notes']
        widgets = {
            'pet': forms.Select(attrs={'id': 'id_pet', 'class': 'form-select'}),
            'procedure': forms.Select(attrs={'id': 'id_procedure', 'class': 'form-select'}),
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'healthcare_provider': forms.TextInput(attrs={'class': 'form-control'}),
            'outcome': forms.TextInput(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'})
        }
        labels = {
            'pet': 'Paciente',
            'procedure': 'Procedimento',
            'date': 'Data da realização',
            'healthcare_provider': 'Responsável pela aplicação/realização',
            'outcome': 'Resultado / Desfecho',
            'notes': 'Observações',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) 

class ExamForm(forms.ModelForm):
    class Meta:
        model = ExamMod
        fields = MedicalEventForm.Meta.fields + ['positive', 'report']
        widgets = {
            **MedicalEventForm.Meta.widgets,
            'positive': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            **MedicalEventForm.Meta.labels,
            'positive': 'Resultado Positivo',
            'report': 'Laudo Médico', 
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['report'].widget.attrs.update({'class': 'form-control'})

class VaccineForm(forms.ModelForm):
    class Meta:
        model = VaccineMod
        fields = MedicalEventForm.Meta.fields + ['batch', 'next_dose']
        widgets = {
            **MedicalEventForm.Meta.widgets,
            'batch': forms.TextInput(attrs={'class': 'form-control'}),
            'next_dose': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
        }
        labels = {
            **MedicalEventForm.Meta.labels,
            'batch': 'Lote',
            'next_dose': 'Próxima Dose',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) 


class MedicationForm(forms.ModelForm):
    class Meta:
        model = MedicationMod
        fields = MedicalEventForm.Meta.fields + ['medicine', 'dosage', 'frequency', 'duration']
        widgets = {
            **MedicalEventForm.Meta.widgets,
            'medicine': forms.Select(attrs={'class': 'form-select'}),
            'dosage': forms.NumberInput(attrs={'class': 'form-control'}),
            'frequency': forms.NumberInput(attrs={'class': 'form-control'}),
            'duration': forms.NumberInput(attrs={'class': 'form-control'})            
        }
        labels = {
            **MedicalEventForm.Meta.labels,
            'medicine': 'Medicamento',
            'dosage': 'Dosagem',
            'frequency': 'Frequência (dias)',
            'duration': 'Duração (dias)',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) 
