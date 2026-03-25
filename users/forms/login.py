from django import forms
from utils.django_forms import add_placeholder


class LoginForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['username'], 'Digite seu nome de usuário')
        add_placeholder(self.fields['password'], 'Digite sua senha')

    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control mx-auto text-center'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control mx-auto text-center'}),
    )