from django import forms
from .models import CatalogMod, StockMod


class CatalogForm(forms.ModelForm):
    class Meta:
        model = CatalogMod
        fields = ['primary_name', 'concentration_value', 'concentration_unity', 'presentation', 'assoc_concentration', 'animal_weight_conc', 'spec_concentration', 'item_type', 'min_stock']
        widgets = {
            'primary_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome do produto'}),
            'concentration_value': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.0001'}),
            'concentration_unity': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Unidade de concentração'}),
            'presentation': forms.Select(attrs={'class': 'form-select'}),
            'assoc_concentration': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'animal_weight_conc': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'spec_concentration': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Concentração específica (JSON)', 'rows': 3}),
            'item_type': forms.Select(attrs={'class': 'form-select'}),
            'min_stock': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class StockForm(forms.ModelForm):
    class Meta:
        model = StockMod
        fields = ['catalog', 'secondary_name', 'batch_number', 'stocking_unity', 'expiry', 'sku_qty', 'dosage_qty']
        widgets = {
            'catalog': forms.Select(attrs={'class': 'form-select'}),
            'secondary_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome secundário do produto'}),
            'batch_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Número do lote'}),
            'stocking_unity': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Unidade de estoque'}),
            'expiry': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'sku_qty': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'SKU'}),
            'dosage_qty': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Quantidade de dosagem'}),
        }