from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from accounts.models import Company, Candidate

User = get_user_model()

class AccountsViewsTest(TestCase):

    def setUp(self):
        pass

    def test_company_signup_view_get(self):
        response = self.client.get(reverse('accounts:company_signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/company_signup.html')
    
    def test_company_signup_view_post_valid(self):
        user_count_before = User.objects.count()
        company_count_before = Company.objects.count()

        valid_data = {
            'email': 'new_company@test.com',
            'password': 'StrongPass!123',
            'password2': 'StrongPass!123',
            'name': 'Nova Empresa Teste'
        }
        response = self.client.post(reverse('accounts:company_signup'), data=valid_data, follow=True)

        self.assertEqual(User.objects.count(), user_count_before + 1)
        self.assertEqual(Company.objects.count(), company_count_before + 1)
        
        self.assertRedirects(response, reverse('jobs:job_list'))
        
        new_user = User.objects.get(email='new_company@test.com')
        self.assertTrue(hasattr(new_user, 'company'))
        self.assertEqual(new_user.company.name, 'Nova Empresa Teste')

    def test_company_signup_view_post_invalid(self):
        user_count_before = User.objects.count()
        company_count_before = Company.objects.count()

        invalid_data = {
            'email': 'invalid_email',
            'password': 'StrongPass!123',
            'password2': 'StrongPass!123',
            'name': 'Nova Empresa Teste'
        }
        response = self.client.post(reverse('accounts:company_signup'), data=invalid_data)

        self.assertEqual(User.objects.count(), user_count_before)
        self.assertEqual(Company.objects.count(), company_count_before)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/company_signup.html')
        self.assertIn('form', response.context)
        self.assertFalse(response.context['form'].is_valid())
        self.assertIn('email', response.context['form'].errors)

    def test_candidate_signup_view_get(self):
        response = self.client.get(reverse('accounts:candidate_signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/candidate_signup.html')
        
    def test_candidate_signup_view_post_valid(self):
        user_count_before = User.objects.count()
        candidate_count_before = Candidate.objects.count()

        valid_data = {
            'email': 'new_candidate@test.com',
            'password': 'StrongPass!123',
            'password2': 'StrongPass!123',
            'last_education': Candidate.Education.SUPERIOR,
            'experience': 'Experiência com Python.'
        }
        response = self.client.post(reverse('accounts:candidate_signup'), data=valid_data, follow=True)

        self.assertEqual(User.objects.count(), user_count_before + 1)
        self.assertEqual(Candidate.objects.count(), candidate_count_before + 1)
        
        self.assertRedirects(response, reverse('jobs:job_list'))

        new_user = User.objects.get(email='new_candidate@test.com')
        self.assertTrue(hasattr(new_user, 'candidate'))
        self.assertEqual(new_user.candidate.last_education, Candidate.Education.SUPERIOR)

    def test_candidate_signup_view_post_invalid(self):
        user_count_before = User.objects.count()
        candidate_count_before = Candidate.objects.count()
        
        invalid_data = {
            'email': 'candidato@test.com',
            'password': '123',
            'password2': '123',
            'last_education': Candidate.Education.SUPERIOR,
        }
        response = self.client.post(reverse('accounts:candidate_signup'), data=invalid_data)

        self.assertEqual(User.objects.count(), user_count_before)
        self.assertEqual(Candidate.objects.count(), candidate_count_before)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/candidate_signup.html')
        self.assertIn('form', response.context)
        self.assertFalse(response.context['form'].is_valid())
        self.assertIn('password', response.context['form'].errors)

    def test_logged_in_user_redirects_on_signup(self):
        user = User.objects.create_user(email='user_already_logged@test.com', password='StrongPass!123')
        
        self.client.login(email='user_already_logged@test.com', password='StrongPass!123')
        
        response_company = self.client.get(reverse('accounts:company_signup'))
        self.assertRedirects(response_company, reverse('jobs:job_list'))
        
        response_candidate = self.client.get(reverse('accounts:candidate_signup'))
        self.assertRedirects(response_candidate, reverse('jobs:job_list'))