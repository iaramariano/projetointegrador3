from django import forms
from .models import ProcedCatalogMod, MedicalEventMod, VaccineMod





# Formulário para cadastro de procedimentos

class CatalogForm(forms.ModelForm):

    species_choices = ProcedCatalogMod.SPECIES_CHOICES
    species_choices.append(('TODAS', 'Todas'))


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
         widget= forms.CheckboxInput(attrs={'class': 'form-check-input'})
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
        widget = forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder':'Breve descrição do procedimento'})
    )
    
    class Meta:
        model = ProcedCatalogMod
        fields = ['name', 'type', 'species', 'min_application', 'min_interval', 'repetition', 'mandatory', 'alternatives', 'description']
        
    def __init__(self, *args, **kwargs):
        
        super().__init__(*args, **kwargs)
        
    def clean_name(self):
        name = self.cleaned_data.get('name', '')
        return name.capitalize()