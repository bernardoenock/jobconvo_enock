from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import login
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .forms import CompanySignUpForm, CandidateSignUpForm

def redirect_if_logged_in(view_func):
    """
    Decorator customizado para redirecionar usuários logados
    para a página principal, evitando que acessem as telas
    de cadastro e login novamente.
    """
    def _wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('jobs:job_list') # Ou para a URL de sua preferência
        return view_func(request, *args, **kwargs)
    return _wrapper

@method_decorator(redirect_if_logged_in, name='dispatch')
class CompanySignUpView(View):
    form_class = CompanySignUpForm
    template_name = 'accounts/company_signup.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) # Faz o login do usuário
            return redirect('jobs:job_list')
        return render(request, self.template_name, {'form': form})

@method_decorator(redirect_if_logged_in, name='dispatch')
class CandidateSignUpView(View):
    form_class = CandidateSignUpForm
    template_name = 'accounts/candidate_signup.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) # Faz o login do usuário
            return redirect('jobs:job_list')
        return render(request, self.template_name, {'form': form})