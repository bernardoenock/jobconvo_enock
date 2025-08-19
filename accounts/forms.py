from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Company, Candidate

class CompanySignUpForm(UserCreationForm):
  company_name = forms.CharField(max_length=255)

  class Meta(UserCreationForm.Meta):
    model = User
    fields = ('email',)

  def save(self, commit=True):
    user = super().save(commit=False)
    user.email = self.cleaned_data['email']
    if commit:
      user.save()
      Company.objects.create(user=user, name=self.cleaned_data['company_name'])
    return user

class CandidateSignUpForm(UserCreationForm):
  class Meta(UserCreationForm.Meta):
    model = User
    fields = ('email',)

  def save(self, commit=True):
    user = super().save(commit=False)
    user.email = self.cleaned_data['email']
    if commit:
      user.save()
      Candidate.objects.create(user=user)
    return user