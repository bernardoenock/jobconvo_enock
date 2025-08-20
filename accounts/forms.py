from django import forms
from django.contrib.auth import get_user_model, password_validation
from django.core.exceptions import ValidationError
from django.db import transaction
from .models import Company, Candidate

User = get_user_model()

class CompanySignUpForm(forms.ModelForm):
    password = forms.CharField(label="Senha", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirme a Senha", widget=forms.PasswordInput)
    name = forms.CharField(max_length=255)

    class Meta:
        model = User
        fields = ('email',)

    def clean_password2(self):
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password and password2 and password != password2:
            raise forms.ValidationError("As senhas não coincidem.")
        return password2

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        if password:
            try:
                password_validation.validate_password(password, self.instance)
            except ValidationError as error:
                self.add_error('password', error)
        return cleaned_data
        
    def save(self, commit=True):
        if not self.cleaned_data.get('email'):
            raise ValueError('Email não pode ser nulo.')

        if not self.cleaned_data.get('password'):
            raise ValueError('Senha não pode ser nula.')
            
        with transaction.atomic():
            user = User.objects.create_user(
                email=self.cleaned_data['email'],
                password=self.cleaned_data['password'],
                is_company=True
            )
            
            Company.objects.create(
                user=user,
                name=self.cleaned_data['name']
            )

        return user

class CandidateSignUpForm(forms.ModelForm):
    password = forms.CharField(label="Senha", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirme a Senha", widget=forms.PasswordInput)
    last_education = forms.ChoiceField(choices=Candidate.Education.choices)
    experience = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model = User
        fields = ('email',)

    def clean_password2(self):
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password and password2 and password != password2:
            raise forms.ValidationError("As senhas não coincidem.")
        return password2

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        if password:
            try:
                password_validation.validate_password(password, self.instance)
            except ValidationError as error:
                self.add_error('password', error)
        return cleaned_data
        
    def save(self, commit=True):
        if not self.cleaned_data.get('email'):
            raise ValueError('Email não pode ser nulo.')

        if not self.cleaned_data.get('password'):
            raise ValueError('Senha não pode ser nula.')
        
        with transaction.atomic():
            user = User.objects.create_user(
                email=self.cleaned_data['email'],
                password=self.cleaned_data['password'],
                is_candidate=True
            )
            
            Candidate.objects.create(
                user=user,
                last_education=self.cleaned_data['last_education'],
                experience=self.cleaned_data['experience']
            )

        return user