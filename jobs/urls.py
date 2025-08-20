from django.urls import path
from . import views

app_name = 'jobs'

urlpatterns = [
  path('', views.JobListView.as_view(), name='job_list'),
  path('jobs/create/', views.JobCreateView.as_view(), name='job_create'),
  path('jobs/<int:pk>/', views.JobDetailView.as_view(), name='job_detail'),
  path('jobs/<int:pk>/edit/', views.JobUpdateView.as_view(), name='job_update'),
  path('jobs/<int:pk>/delete/', views.JobDeleteView.as_view(), name='job_delete'),

  path('jobs/<int:pk>/apply/', views.apply_to_job, name='apply'),

  path('reports/', views.reports, name='reports'),
  path('reports/data/jobs-per-month/', views.jobs_per_month, name='jobs_per_month'),
  path('reports/data/apps-per-month/', views.apps_per_month, name='apps_per_month'),
]