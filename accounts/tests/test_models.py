from django.test import TestCase
from accounts.models import User, Company, Candidate

class UserModelTest(TestCase):
    """
    Testa a criação do modelo de usuário customizado.
    """
    def test_create_user_with_email(self):
        """
        Verifica se um usuário é criado corretamente com o email como username.
        """
        user = User.objects.create_user(email='teste@email.com', password='password123')
        self.assertEqual(user.email, 'teste@email.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        try:
            # username não deve existir
            self.assertIsNone(user.username)
        except AttributeError:
            pass
        with self.assertRaises(TypeError):
            User.objects.create_user()
        with self.assertRaises(ValueError):
            User.objects.create_user(email='')

    def test_create_superuser(self):
        """
        Verifica se um superusuário é criado corretamente.
        """
        admin_user = User.objects.create_superuser(email='admin@email.com', password='password123')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        self.assertEqual(str(admin_user), 'admin@email.com')

class CompanyModelTest(TestCase):
    """
    Testa o modelo Company e sua relação com o User.
    """
    def setUp(self):
        self.user = User.objects.create_user(email='empresa@teste.com', password='password123')

    def test_create_company(self):
        """
        Verifica se uma empresa é criada corretamente e se a relação OneToOne com o User funciona.
        """
        company = Company.objects.create(user=self.user, name='Empresa de Exemplo S.A.')
        self.assertEqual(company.name, 'Empresa de Exemplo S.A.')
        self.assertEqual(company.user, self.user)
        self.assertEqual(str(company), 'Empresa de Exemplo S.A.')
        self.assertEqual(self.user.company, company)

    def test_delete_user_deletes_company(self):
        """
        Verifica se a exclusão do usuário também exclui a empresa associada,
        graças ao on_delete=models.CASCADE.
        """
        company = Company.objects.create(user=self.user, name='Empresa para Deletar')
        user_id = self.user.id
        self.user.delete()
        with self.assertRaises(Company.DoesNotExist):
            Company.objects.get(user_id=user_id)

class CandidateModelTest(TestCase):
    """
    Testa o modelo Candidate e sua relação com o User.
    """
    def setUp(self):
        self.user = User.objects.create_user(email='candidato@teste.com', password='password123')

    def test_create_candidate(self):
        """
        Verifica se um candidato é criado corretamente e se a relação OneToOne com o User funciona.
        """
        candidate = Candidate.objects.create(
            user=self.user,
            last_education=Candidate.Education.SUPERIOR,
            experience='Experiência profissional de 5 anos.'
        )
        self.assertEqual(candidate.user, self.user)
        self.assertEqual(candidate.last_education, Candidate.Education.SUPERIOR)
        self.assertEqual(candidate.experience, 'Experiência profissional de 5 anos.')
        self.assertEqual(str(candidate), 'candidato@teste.com')
        self.assertEqual(self.user.candidate, candidate)

    def test_candidate_default_education(self):
        """
        Verifica se o valor padrão para last_education é 'Ensino médio'.
        """
        candidate = Candidate.objects.create(user=self.user)
        self.assertEqual(candidate.last_education, Candidate.Education.MEDIO)

    def test_delete_user_deletes_candidate(self):
        """
        Verifica se a exclusão do usuário também exclui o candidato associado,
        graças ao on_delete=models.CASCADE.
        """
        candidate = Candidate.objects.create(user=self.user, last_education=Candidate.Education.MEDIO)
        user_id = self.user.id
        self.user.delete()
        with self.assertRaises(Candidate.DoesNotExist):
            Candidate.objects.get(user_id=user_id)