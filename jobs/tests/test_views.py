from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from datetime import datetime
from accounts.models import Candidate, User, Company
from jobs.models import Application, Job

class JobViewTest(TestCase):
    def setUp(self):
        self.company_user = User.objects.create_user(email='empresa@teste.com', password='StrongPass!123')
        self.company = Company.objects.create(user=self.company_user, name='Empresa Teste')
        self.candidate_user = User.objects.create_user(email='candidato@teste.com', password='StrongPass!123')
        self.candidate = Candidate.objects.create(user=self.candidate_user, last_education=Candidate.Education.MEDIO)

    def test_job_list_view(self):
        """Verifica se a view JobListView retorna 200 OK e usa o template correto."""
        response = self.client.get(reverse('jobs:job_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'jobs/job_list.html')
        
    def test_job_create_view_access(self):
        """Verifica se apenas empresas logadas podem acessar a página de criação de vaga."""
        response = self.client.get(reverse('jobs:job_create'))
        self.assertRedirects(response, f'{reverse("accounts:login")}?next=/jobs/create/')
        
        self.client.login(email='candidato@teste.com', password='StrongPass!123')
        response = self.client.get(reverse('jobs:job_create'))
        self.assertEqual(response.status_code, 403)
        
        self.client.login(email='empresa@teste.com', password='StrongPass!123')
        response = self.client.get(reverse('jobs:job_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'jobs/job_form.html')

    def test_job_create_view_post_valid_data(self):
        """Verifica se a submissão de dados válidos cria uma nova vaga."""
        self.client.login(email='empresa@teste.com', password='StrongPass!123')
        job_count_before = Job.objects.count()
        
        valid_data = {
            'title': 'Desenvolvedor Python',
            'salary_band': Job.SalaryBand.FROM_2K_TO_3K,
            'requirements': 'Experiência com Django.',
            'min_education': Job.MinEducation.SUPERIOR
        }
        
        response = self.client.post(reverse('jobs:job_create'), data=valid_data, follow=True)
        
        job_count_after = Job.objects.count()
        self.assertEqual(job_count_after, job_count_before + 1)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'jobs/job_detail.html')
        self.assertTrue(Job.objects.filter(title='Desenvolvedor Python').exists())

    def test_job_create_view_post_invalid_data(self):
        """Verifica se a submissão de dados inválidos não cria uma vaga."""
        self.client.login(email='empresa@teste.com', password='StrongPass!123')
        job_count_before = Job.objects.count()
        
        invalid_data = {
            'title': '',
            'salary_band': Job.SalaryBand.FROM_2K_TO_3K,
            'requirements': 'Experiência com Django.',
            'min_education': Job.MinEducation.SUPERIOR
        }
        
        response = self.client.post(reverse('jobs:job_create'), data=invalid_data)
        
        job_count_after = Job.objects.count()
        self.assertEqual(job_count_after, job_count_before)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'jobs/job_form.html')
        self.assertIn('form', response.context)
        self.assertFalse(response.context['form'].is_valid())
        self.assertIn('title', response.context['form'].errors)

    def test_apply_to_job_post_valid_data(self):
        """Verifica se a submissão de dados válidos cria uma Application."""
        self.client.login(email='candidato@teste.com', password='StrongPass!123')
        job = Job.objects.create(
            company=self.company,
            title='Vaga de Teste',
            salary_band=Job.SalaryBand.FROM_1K_TO_2K,
            min_education=Job.MinEducation.SUPERIOR,
            requirements='Requisitos de teste.'
        )
        application_count_before = Application.objects.count()

        valid_data = {
            'salary_expectation': 1500.00,
            'candidate_last_education': Candidate.Education.SUPERIOR,
            'candidate_experience': 'Experiência de teste.'
        }
        response = self.client.post(reverse('jobs:apply', args=[job.pk]), data=valid_data, follow=True)

        application_count_after = Application.objects.count()
        self.assertEqual(application_count_after, application_count_before + 1)
        self.assertEqual(response.status_code, 200) # Redireciona para o detalhe da vaga
        self.assertTrue(Application.objects.filter(job=job).exists())

    def test_job_detail_view_shows_applicants_to_company(self):
        """Empresa deve ver os candidatos que se aplicaram à sua vaga."""
        self.client.login(email='empresa@teste.com', password='StrongPass!123')
        job = Job.objects.create(
            company=self.company,
            title='Vaga de Teste',
            salary_band=Job.SalaryBand.FROM_1K_TO_2K,
            min_education=Job.MinEducation.SUPERIOR,
            requirements='Requisitos de teste.'
        )
        
        candidate_user = User.objects.create_user(email='candidato_aplicado@teste.com', password='StrongPass!123')
        candidate = Candidate.objects.create(user=candidate_user, last_education=Candidate.Education.SUPERIOR)
        Application.objects.create(
            job=job,
            candidate=candidate,
            salary_expectation=1500.00,
            candidate_last_education=Candidate.Education.SUPERIOR
        )

        response = self.client.get(reverse('jobs:job_detail', args=[job.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Candidatos')
        self.assertContains(response, 'candidato_aplicado@teste.com')
        self.assertContains(response, '<strong>Pontuação:</strong> 2')

    def test_jobs_per_month_data(self):
      """Verifica se a view de dados de vagas por mês retorna o JSON correto."""
      
      Job.objects.create(
          company=self.company, 
          title='Vaga Jan', 
          salary_band=1, 
          min_education=1, 
          created_at=timezone.datetime(2025, 1, 15, tzinfo=timezone.utc)
      )
      Job.objects.create(
          company=self.company, 
          title='Vaga Jan', 
          salary_band=1, 
          min_education=1, 
          created_at=timezone.datetime(2025, 1, 20, tzinfo=timezone.utc)
      )
      Job.objects.create(
          company=self.company, 
          title='Vaga Fev', 
          salary_band=1, 
          min_education=1, 
          created_at=timezone.datetime(2025, 2, 10, tzinfo=timezone.utc)
      )

      client = self.client
      client.login(email='empresa@teste.com', password='StrongPass!123')
      
      response = client.get(reverse('jobs:jobs_per_month'))
      self.assertEqual(response.status_code, 200)
      data = response.json()
      self.assertEqual(data['labels'], ['2025-01', '2025-02'])
      self.assertEqual(data['datasets'][0]['data'], [2, 1])

    def test_candidates_per_month_data(self):
        """Verifica se a view de candidatos por mês retorna o JSON correto."""

        job = Job.objects.create(
            company=self.company,
            title='Vaga Teste',
            salary_band=Job.SalaryBand.FROM_1K_TO_2K,
            min_education=Job.MinEducation.SUPERIOR,
            requirements='Requisitos de teste.'
        )

        candidate_user_jan = User.objects.create_user(email='jan@teste.com', password='StrongPass!123')
        candidate_jan = Candidate.objects.create(user=candidate_user_jan, last_education=Candidate.Education.MEDIO)
        Application.objects.create(
            job=job,
            candidate=candidate_jan,
            salary_expectation=1200,
            candidate_last_education=Candidate.Education.MEDIO,
            created_at=timezone.datetime(2025, 1, 10, tzinfo=timezone.utc)
        )

        candidate_user_feb = User.objects.create_user(email='feb@teste.com', password='StrongPass!123')
        candidate_feb = Candidate.objects.create(user=candidate_user_feb, last_education=Candidate.Education.SUPERIOR)
        Application.objects.create(
            job=job,
            candidate=candidate_feb,
            salary_expectation=1500,
            candidate_last_education=Candidate.Education.SUPERIOR,
            created_at=timezone.datetime(2025, 2, 5, tzinfo=timezone.utc)
        )

        self.client.login(email='empresa@teste.com', password='StrongPass!123')
        response = self.client.get(reverse('jobs:candidates_per_month'))

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['labels'], ['2025-01', '2025-02'])
        self.assertEqual(data['datasets'][0]['data'], [1, 1])


    def test_my_job_list_view_shows_only_company_jobs(self):
        """Verifica se a view 'my_jobs' mostra apenas vagas da empresa logada."""
        job1 = Job.objects.create(
            company=self.company,
            title='Vaga Empresa Logada 1',
            salary_band=Job.SalaryBand.FROM_1K_TO_2K,
            min_education=Job.MinEducation.SUPERIOR,
            requirements='Requisitos 1'
        )
        job2 = Job.objects.create(
            company=self.company,
            title='Vaga Empresa Logada 2',
            salary_band=Job.SalaryBand.FROM_2K_TO_3K,
            min_education=Job.MinEducation.SUPERIOR,
            requirements='Requisitos 2'
        )

        other_user = User.objects.create_user(email='outra@empresa.com', password='StrongPass!123')
        other_company = Company.objects.create(user=other_user, name='Outra Empresa')
        Job.objects.create(
            company=other_company,
            title='Vaga Outra Empresa',
            salary_band=Job.SalaryBand.FROM_1K_TO_2K,
            min_education=Job.MinEducation.SUPERIOR,
            requirements='Requisitos outra empresa'
        )

        self.client.login(email='empresa@teste.com', password='StrongPass!123')
        response = self.client.get(reverse('jobs:my_jobs'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'jobs/job_list.html')
        jobs_list = list(response.context['jobs'])
        
        self.assertIn(job1, jobs_list)
        self.assertIn(job2, jobs_list)
        self.assertEqual(len(jobs_list), 2)
        self.assertNotIn(Job.objects.get(title='Vaga Outra Empresa'), jobs_list)