from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Count
from django.db.models.functions import TruncMonth
from django.http import JsonResponse, Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from accounts.models import Company, Candidate
from .models import Job, Application
from .forms import JobForm, ApplicationForm

class CompanyRequiredMixin(UserPassesTestMixin):
  def test_func(self):
    return hasattr(self.request.user, 'company')
  
class CandidateRequiredMixin(UserPassesTestMixin):
  def test_func(self):
    return hasattr(self.request.user, 'candidate')
  
class MyJobListView(LoginRequiredMixin, ListView):
    model = Job
    template_name = 'jobs/job_list.html'
    context_object_name = 'jobs'

    def get_queryset(self):
        if hasattr(self.request.user, 'company'):
            return Job.objects.filter(company=self.request.user.company).annotate(app_count=Count('applications')).order_by('-created_at')
        return Job.objects.none()

class JobListView(ListView):
  model = Job
  template_name = 'jobs/job_list.html'
  context_object_name = 'jobs'

  def get_queryset(self):
    return Job.objects.all().annotate(app_count=Count('applications')).order_by('-created_at')
  
class JobDetailView(DetailView):
  model = Job
  template_name = 'jobs/job_detail.html'
  context_object_name = 'job'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    
    if hasattr(self.request.user, 'company') and self.object.company == self.request.user.company:
      context['applications'] = self.object.applications.all().order_by('-score')
      
    return context

class JobCreateView(LoginRequiredMixin, CompanyRequiredMixin, CreateView):
  model = Job
  form_class = JobForm
  template_name = 'jobs/job_form.html'

  def form_valid(self, form):
    form.instance.company = self.request.user.company
    return super().form_valid(form)
  
  def get_success_url(self):
    return reverse_lazy('jobs:job_detail', kwargs={'pk': self.object.pk})

class JobUpdateView(LoginRequiredMixin, CompanyRequiredMixin, UpdateView):
  model = Job
  form_class = JobForm
  template_name = 'jobs/job_form.html'

  def get_queryset(self):
    return Job.objects.filter(company=self.request.user.company)

  def get_success_url(self):
    return reverse_lazy('jobs:job_detail', kwargs={'pk': self.object.pk})

class JobDeleteView(LoginRequiredMixin, CompanyRequiredMixin, DeleteView):
  model = Job
  success_url = reverse_lazy('jobs:job_list')
  template_name = 'jobs/job_confirm_delete.html'

  def get_queryset(self):
    return Job.objects.filter(company=self.request.user.company)

class JobDetailView(DetailView):
    model = Job
    template_name = 'jobs/job_detail.html'
    context_object_name = 'job'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        if hasattr(user, 'company') and self.object.company == user.company:
            context['applications'] = self.object.applications.all().order_by('-score')

        if hasattr(user, 'candidate'):
            context['has_applied'] = self.object.applications.filter(candidate=user.candidate).exists()

        return context

class ApplyView(LoginRequiredMixin, View):
    def get(self, request, pk):
        job = get_object_or_404(Job, pk=pk)

        if not hasattr(request.user, 'candidate'):
            raise Http404("Only candidates can apply.")

        candidate = request.user.candidate

        if Application.objects.filter(job=job, candidate=candidate).exists():
            return redirect('jobs:job_detail', pk=job.pk)

        form = ApplicationForm(initial={
            'candidate_last_education': candidate.last_education,
            'candidate_experience': candidate.experience,
        })

        return render(request, 'jobs/apply.html', {'form': form, 'job': job})

    def post(self, request, pk):
        job = get_object_or_404(Job, pk=pk)

        if not hasattr(request.user, 'candidate'):
            raise Http404("Only candidates can apply.")

        candidate = request.user.candidate
        form = ApplicationForm(request.POST)

        if form.is_valid():
            Application.objects.create(
                job=job,
                candidate=candidate,
                salary_expectation=form.cleaned_data['salary_expectation'],
                candidate_last_education=form.cleaned_data['candidate_last_education'],
                candidate_experience=form.cleaned_data['candidate_experience']
            )
            return redirect('jobs:job_detail', pk=job.pk)

        return render(request, 'jobs/apply.html', {'form': form, 'job': job})


@login_required
def reports(request):
  if not hasattr(request.user, 'company'):
    raise Http404("Only companies can view reports. :(")
  
  return render(request, 'jobs/reports.html')

@login_required
def apply_to_job(request, pk):
  job = get_object_or_404(Job, pk=pk)

  if not hasattr(request.user, 'candidate'):
    raise Http404("Only candidate can apply. :(")
  
  candidate = request.user.candidate
  
  if request.method == 'POST':
    form = ApplicationForm(request.POST)
    if form.is_valid():
      Application.objects.create(
        job=job,
        candidate=candidate,
        salary_expectation=form.cleaned_data['salary_expectation'],
        candidate_last_education=form.cleaned_data['candidate_last_education'],
        candidate_experience=form.cleaned_data['candidate_experience']
      )
      return redirect('jobs:job_detail', pk=job.pk)
  else:
    form = ApplicationForm(initial={
      'candidate_last_education': candidate.last_education,
      'candidate_experience': candidate.experience,
    })

  return render(request, 'jobs/apply.html', {'form': form, 'job': job})


@login_required
def jobs_per_month(request):
  qs = (Job.objects
        .annotate(month=TruncMonth('created_at'))
        .values('month')
        .annotate(count=Count('id'))
        .order_by('month'))
  labels = [q['month'].strftime('%Y-%m') for q in qs]
  data = [q['count'] for q in qs]
  return JsonResponse({'labels': labels, 'datasets': [{'label': 'Vagas por mês', 'data': data}]})


@login_required
def apps_per_month(request):
  qs = (Application.objects
        .annotate(month=TruncMonth('created_at'))
        .values('month')
        .annotate(count=Count('id'))
        .order_by('month'))
  labels = [q['month'].strftime('%Y-%m') for q in qs]
  data = [q['count'] for q in qs]
  return JsonResponse({'labels': labels, 'datasets': [{'label': 'Aplicações por mês', 'data': data}]})

@login_required
def candidates_per_month(request):
    data = (
        Application.objects.annotate(month=TruncMonth('created_at'))
        .values('month')
        .annotate(total=Count('id'))
        .order_by('month')
    )
    labels = [item['month'].strftime('%Y-%m') for item in data]
    counts = [item['total'] for item in data]
    return JsonResponse({
        'labels': labels,
        'datasets': [{
            'label': 'Candidatos por mês',
            'data': counts
        }]
    })