from django.test import TestCase
from accounts.models import User, Company, Candidate
from jobs.models import Job, Application

class ApplicationModelTest(TestCase):
    def setUp(self):
        self.company_user = User.objects.create_user(email='empresa@teste.com', password='password123')
        self.company = Company.objects.create(user=self.company_user, name='Empresa Teste')
        self.job = Job.objects.create(
            company=self.company,
            title='Vaga de Teste',
            salary_band=Job.SalaryBand.FROM_1K_TO_2K,
            min_education=Job.MinEducation.SUPERIOR,
            requirements='Requisitos de teste.'
        )

    def _create_candidate_for_test(self, email_suffix, last_education, experience=''):
        """Helper para criar um candidato único para cada teste."""
        user = User.objects.create_user(email=f'candidato_{email_suffix}@teste.com', password='password123')
        candidate = Candidate.objects.create(
            user=user,
            last_education=last_education,
            experience=experience
        )
        return candidate

    def test_score_calculation(self):
        candidate1 = self._create_candidate_for_test('perfect', Candidate.Education.SUPERIOR)
        application_perfect_match = Application.objects.create(
            job=self.job,
            candidate=candidate1,
            salary_expectation=1500.00,
            candidate_last_education=Candidate.Education.SUPERIOR
        )
        self.assertEqual(application_perfect_match.score, 2)

        candidate2 = self._create_candidate_for_test('education', Candidate.Education.SUPERIOR)
        application_education_match = Application.objects.create(
            job=self.job,
            candidate=candidate2,
            salary_expectation=500.00,
            candidate_last_education=Candidate.Education.SUPERIOR
        )
        self.assertEqual(application_education_match.score, 1)

        candidate3 = self._create_candidate_for_test('salary', Candidate.Education.MEDIO)
        application_salary_match = Application.objects.create(
            job=self.job,
            candidate=candidate3,
            salary_expectation=1500.00,
            candidate_last_education=Candidate.Education.MEDIO
        )
        self.assertEqual(application_salary_match.score, 1)
        
        candidate4 = self._create_candidate_for_test('no_match', Candidate.Education.MEDIO)
        application_no_match = Application.objects.create(
            job=self.job,
            candidate=candidate4,
            salary_expectation=500.00,
            candidate_last_education=Candidate.Education.MEDIO
        )
        self.assertEqual(application_no_match.score, 0)

    def test_salary_fits_band_logic(self):

        job_band_1k = Job.objects.create(
            company=self.company, title='Job 1k', salary_band=Job.SalaryBand.UP_TO_1K, min_education=Job.MinEducation.MEDIO, requirements=''
        )
        app_1k_ok = Application(job=job_band_1k, salary_expectation=999.99)
        self.assertTrue(app_1k_ok._salary_fits_band())
        app_1k_border = Application(job=job_band_1k, salary_expectation=1000.00)
        self.assertTrue(app_1k_border._salary_fits_band())
        app_1k_fail = Application(job=job_band_1k, salary_expectation=1000.01)
        self.assertFalse(app_1k_fail._salary_fits_band())

        job_band_2k = Job.objects.create(
            company=self.company, title='Job 2k', salary_band=Job.SalaryBand.FROM_1K_TO_2K, min_education=Job.MinEducation.MEDIO, requirements=''
        )
        app_2k_border1 = Application(job=job_band_2k, salary_expectation=1000.00)
        self.assertTrue(app_2k_border1._salary_fits_band())
        app_2k_ok = Application(job=job_band_2k, salary_expectation=1500.00)
        self.assertTrue(app_2k_ok._salary_fits_band())
        app_2k_border2 = Application(job=job_band_2k, salary_expectation=2000.00)
        self.assertTrue(app_2k_border2._salary_fits_band())
        app_2k_fail = Application(job=job_band_2k, salary_expectation=2000.01)
        self.assertFalse(app_2k_fail._salary_fits_band())
        
        job_band_3k = Job.objects.create(
            company=self.company, title='Job 3k', salary_band=Job.SalaryBand.FROM_2K_TO_3K, min_education=Job.MinEducation.MEDIO, requirements=''
        )
        app_3k_border1 = Application(job=job_band_3k, salary_expectation=2000.00)
        self.assertTrue(app_3k_border1._salary_fits_band())
        app_3k_ok = Application(job=job_band_3k, salary_expectation=2500.00)
        self.assertTrue(app_3k_ok._salary_fits_band())
        app_3k_border2 = Application(job=job_band_3k, salary_expectation=3000.00)
        self.assertTrue(app_3k_border2._salary_fits_band())
        app_3k_fail = Application(job=job_band_3k, salary_expectation=3000.01)
        self.assertFalse(app_3k_fail._salary_fits_band())

        job_band_above3k = Job.objects.create(
            company=self.company, title='Job 3k+', salary_band=Job.SalaryBand.ABOVE_3K, min_education=Job.MinEducation.MEDIO, requirements=''
        )
        app_above3k_fail = Application(job=job_band_above3k, salary_expectation=3000.00)
        self.assertFalse(app_above3k_fail._salary_fits_band())
        app_above3k_ok = Application(job=job_band_above3k, salary_expectation=3000.01)
        self.assertTrue(app_above3k_ok._salary_fits_band())
