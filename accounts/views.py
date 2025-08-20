from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import CompanySignUpForm, CandidateSignUpForm

def company_signup(request):
  if request.method == 'POST':
    form = CompanySignUpForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('jobs:job_list')
  
  else:
    form = CompanySignUpForm()
  
  return render(request, 'accounts/signup_form.html', {'form': form})


def candidate_signup(request):
  if request.method == 'POST':
    form = CandidateSignUpForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('jobs:job_list')
  
  else:
    form = CandidateSignUpForm()
  
  return render(request, 'accounts/signup_form.html', {'form': form})
