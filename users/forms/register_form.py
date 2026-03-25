import re

from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from utils.django_forms import add_attr, add_placeholder, strong_password
from django.utils.safestring import mark_safe


class RegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['username'], 'Nome de usuário')
        add_placeholder(self.fields['email'], 'E-mail do usuário')
        add_placeholder(self.fields['first_name'], 'Ex.: João')
        add_placeholder(self.fields['last_name'], 'Ex.: Silva')
        add_placeholder(self.fields['password'], 'Digite a senha')
        add_placeholder(self.fields['password2'], 'Repita a senha')

    username = forms.CharField(
        label='Nome de usuário',
        help_text=mark_safe(
            'O nome de usuário pode ter letras, números ou um dos seguintes caracteres: @.+-_.<br>'
            'Deve ter de 4 a 150 caracteres.'
        ),
        error_messages={
            'required': 'Esse campo não pode estar em branco',
            'min_length': 'O nome de usuário deve ter mais de 4 caracteres',
            'max_length': 'O nome de usuário deve ter menos de 150 caracteres',
            'unique': 'Já existe um usuário com esse nome de usuário'
        },
        min_length=4, max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control mx-auto w-75 text-center'})
    )
    first_name = forms.CharField(
        error_messages={'required': 'Digite o primeiro nome'},
        label='Nome',
        widget=forms.TextInput(attrs={'class': 'form-control mx-auto w-75 text-center'})
    )
    last_name = forms.CharField(
        error_messages={'required': 'Digite o sobrenome'},
        label='Sobrenome',
        widget=forms.TextInput(attrs={'class': 'form-control mx-auto w-75 text-center'})
    )
    email = forms.EmailField(
        error_messages={'required': 'E-mail é obrigatório'},
        label='E-mail',
        help_text='Insira um e-mail válido',
        widget=forms.EmailInput(attrs={'class': 'form-control mx-auto w-75 text-center'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control mx-auto w-75 text-center'}),
        error_messages={
            'required': 'Senha não pode ficar em branco'
        },
        help_text=mark_safe(
            'A senha deve ter pelo menos uma letra maiúscula,'
            'uma letra minúscula e um número.<br>A senha deve ter'
            'no mínimo 8 caracteres'
        ),
        validators=[strong_password],
        label='Senha'
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control mx-auto w-75 text-center'}),
        label='Confirme sua senha',
        error_messages={
            'required': 'Por favor, repita sua senha'
        },
    )

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
        ]

    def clean_email(self):
        email = self.cleaned_data.get('email', '')
        exists = User.objects.filter(email=email).exists()

        if exists:
            raise ValidationError(
                'E-mail já utilizado', code='invalid',
            )

        return email

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password != password2:
            password_confirmation_error = ValidationError(
                'A senha e sua confirmação devem ser idênticas',
                code='invalid'
            )
            raise ValidationError({
                'password': password_confirmation_error,
                'password2': [
                    password_confirmation_error,
                ],
            })