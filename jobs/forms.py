from django import forms
from .models import Job, Application
from accounts.models import Candidate

class JobForm(forms.ModelForm):
  class Meta:
    model = Job
    fields = ('title', 'salary_band', 'requirements', 'min_education')

class ApplicationForm(forms.ModelForm):
  class Meta:
    model = Application
    fields = ('salary_expectation', 'candidate_last_education', 'candidate_experience')

  def __init__(self, *args, **kwargs):
    self.candidate: Candidate = kwargs.pop('candidate', None)
    self.job = kwargs.pop('job', None)
    super().__init__(*args, **kwargs)

  def save(self, commit=True):
    app = super().save(commit=False)
    app.candidate = self.candidate
    app.job = self.job
    
    if commit:
      app.save()

    return app