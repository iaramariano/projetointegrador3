from django import forms
from django.utils import timezone
from .models import PetsMod, MedicalEventMod
#from .utils import MEDICAL_EVENTS_SECTOR

# *********************************************FORMULÁRIO PARA REGISTRO DE CÃES*********************************************

class PetsModForm(forms.ModelForm):
    class Meta:
        model = PetsMod
        fields = ['species', 'name', 'sex', 'age', 
                  'arrival', 'arrival_date', 'placement', 
                  'history', 'chip', 'status', 'photo']
                  
        widgets = {'species': forms.RadioSelect(attrs={'class': 'form-check-input ms-3 me-2'}),
                   'name': forms.TextInput(attrs={'class': 'form-control text-center form-field-lg', 'placeholder': 'Nome do Animal'}),
                   'sex': forms.RadioSelect(attrs={'class': 'form-check-input ms-3 me-2'}),
                   
                   'age': forms.TextInput(attrs={'class': 'form-control text-center form-field-md', 'value': 'Idade do Animal'}),
                   'arrival': forms.Select(attrs={'class': 'form-select text-center form-field-md'}),
                   'arrival_date': forms.DateField(),
                   'placement': forms.Select(attrs={'class': 'form-select text-center form-field-md'}),                                                                             

                    'history': forms.Textarea(attrs={'class': 'form-control text-center', 'placeholder': 'Histórico do Animal'}),
                    'chip': forms.TextInput(attrs={'class': 'form-control text-center form-field-md', 'value': 'Número do chip'}),
                   'status': forms.Select(attrs={'class': 'form-select text-center form-field-md'})
                    }
    
    def __init__(self, *args, **kwargs):
        
        super().__init__(*args, **kwargs)
        self.fields['sex'].empty_label = None
        self.fields['sex'].required = True
        self.fields['front_photo'].widget.initial_text = 'Foto atual'
        self.fields['front_photo'].widget.input_text = 'Escolher outra'

    def clean_name(self):
        name = self.cleaned_data.get('name', '')
        return name.capitalize()

# *********************************************FORMULÁRIO PARA REGISTRO DE SETORES*********************************************


'''class SectorModForm(forms.ModelForm):
    class Meta:
        model = SectorMod
        fields = ['name', 'type']
        widgets = {'name': forms.TextInput(attrs={'class': 'form-control text-center field-add-sector', 'placeholder': 'Nome do setor'}),
                     'type': forms.Select(attrs={'class': 'form-select text-center field-add-type'})        
                   }
        
    def clean_name(self):
        name = self.cleaned_data.get('name', '')
        return name.capitalize()
       '''
#******************************************FORMULÁRIO PARA CADASTRO DE EVENTO MÉDICO PARA UM PET**********************************************


class MedicalEventForm(forms.ModelForm):
    event = forms.CharField(
        min_length=5,
        max_length=200,
        widget=forms.Textarea(attrs={
            "rows": 3,
            "cols": 40,
            "class": "form-control text-center form-field-lg",
            "placeholder": "Descreva o evento médico",
            "minlength": 5,
            "maxlength": 200,
        })
    )

    patients_list = PetsMod.objects.all().order_by('name')
    patient = forms.ModelChoiceField(queryset=patients_list, label='CÃO', 
                                     widget=forms.Select(attrs={'class': 'form-select text-center form-field-md', 'required': 'true'}))

    class Meta:
        model = MedicalEventMod
        fields = ['patient','event','event_date','change_status']
        widgets = {'event_date': forms.DateInput(attrs={'class': 'form-control text-center form-field-md', 'type': 'date', 'value': '', 'required': 'true'}),
                   'change_status': forms.CheckboxInput(attrs={'class': 'form-check-input'})
                   }
        labels = {'event_date': 'DATA DO EVENTO', 'change_status': 'ALTERAR SITUAÇÃO DO CÃO', 'patient': 'CÃO', 'event': 'EVENTO MÉDICO'}
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['event_date'].widget.attrs['max'] = timezone.localdate().isoformat()

    def clean_event_date(self):
        d = self.cleaned_data.get('event_date')
        if d and d > timezone.localdate():
            raise forms.ValidationError("Data no futuro não é permitida.")
        return d
    
#***************************************************FORMULÁRIO PARA ALTERAÇÃO DE STATUS DO PET)****************************************** 
#******************************************************(AUXILIAR AO DO EVENTO MÉDICO)***************************************************

class NewStatusForm(forms.ModelForm):
    class Meta:
        model = PetsMod
        fields = ['status']
        widgets = {'status': forms.Select(attrs={'class': 'form-select text-center form-field-md'})}
        labels = {'status': 'ALTERAR SITUAÇÃO DO CÃO PARA:'}

#******************************************FORMULÁRIO PARA CADASTRO DE EVENTO MÉDICO PARA UM SETOR***************************************

'''class MedicalEventSectorForm(forms.ModelForm):
    event = forms.ChoiceField(choices=MEDICAL_EVENTS_SECTOR, label='EVENTO MÉDICO', widget=forms.Select(attrs={'class': 'form-select text-center form-field-md', 'required': 'true'}))

    class Meta:
        model = MedicalEventMod
        fields = ['event','event_date']
        widgets = {
                   'event_date': forms.DateInput(attrs={'class': 'form-control text-center form-field-md', 'type': 'date', 'value': '', 'required': 'true'})
                   }
        labels = {'event_date': 'DATA DO EVENTO'}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['event_date'].widget.attrs['max'] = timezone.localdate().isoformat()

    def clean_event_date(self):
        d = self.cleaned_data.get('event_date')
        if d and d > timezone.localdate():
            raise forms.ValidationError("Data no futuro não é permitida.")
        return d

#**************************************************FORMULÁRIO PARA SELEÇÃO DE SETOR********************************************************
#************************************************(AUXILIAR AO DO EVENTO MÉDICO DE SETOR)***************************************************

class SectorSelectForm(forms.ModelForm):
    class Meta:
        model = PetsMod
        
        sector_list = SectorMod.objects.all().order_by('name')
        sector = forms.ModelChoiceField(queryset=sector_list, label='SETOR', 
                                     widget=forms.Select(attrs={'class': 'form-select text-center form-field-md', 'required': 'true'}))
        fields = ['sector']'''