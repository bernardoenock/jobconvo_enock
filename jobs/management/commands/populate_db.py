import random
from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker
from django.contrib.auth import get_user_model
from accounts.models import Company, Candidate
from jobs.models import Job, Application

fake = Faker()
User = get_user_model()

NUM_COMPANIES = 10
NUM_CANDIDATES = 500
NUM_JOBS = 1000
MAX_APPS_PER_JOB = 10

PASSWORD = '@T3star123'

education_choices = [
    Job.MinEducation.FUNDAMENTAL,
    Job.MinEducation.MEDIO,
    Job.MinEducation.TECNOLOGO,
    Job.MinEducation.SUPERIOR,
    Job.MinEducation.POS_MBA_MESTRADO,
    Job.MinEducation.DOUTORADO
]

salary_bands = {
    Job.SalaryBand.UP_TO_1K: (500, 1000),
    Job.SalaryBand.FROM_1K_TO_2K: (1000, 2000),
    Job.SalaryBand.FROM_2K_TO_3K: (2000, 3000),
    Job.SalaryBand.ABOVE_3K: (3001, 8000),
}

class Command(BaseCommand):
    help = 'Populates the database with companies, candidates, jobs and applications.'

    def handle(self, *args, **kwargs):
        self.stdout.write("Populating database... pode demorar alguns minutos.")
        companies = self.create_companies()
        candidates = self.create_candidates()
        jobs = self.create_jobs(companies)
        self.create_applications(jobs, candidates)

        company = random.choice(companies)
        self.stdout.write(self.style.SUCCESS(
            f"\n✅ Pronto! Você pode logar com a empresa: -> email: {company.user.email} / password: {PASSWORD}"
        ))

    def create_companies(self):
        companies = []
        for _ in range(NUM_COMPANIES):
            email = fake.unique.company_email()
            user = User.objects.create_user(
                email=email,
                password=PASSWORD,
                is_company=True
            )
            company = Company.objects.create(user=user, name=fake.company())
            companies.append(company)
        return companies

    def create_candidates(self):
        candidates = []
        for _ in range(NUM_CANDIDATES):
            email = fake.unique.email()
            user = User.objects.create_user(
                email=email,
                password=PASSWORD,
                is_candidate=True
            )
            candidate = Candidate.objects.create(
                user=user,
                last_education=random.choice(education_choices),
                experience=fake.text(max_nb_chars=200)
            )
            candidates.append(candidate)
        return candidates

    def create_jobs(self, companies):
        jobs = []
        for _ in range(NUM_JOBS):
            company = random.choice(companies)
            salary_band = random.choice(list(Job.SalaryBand))
            created_at = timezone.now() - timedelta(days=random.randint(0, 365))
            job = Job.objects.create(
                company=company,
                title=fake.job(),
                salary_band=salary_band,
                requirements=fake.text(max_nb_chars=200),
                min_education=random.choice(education_choices),
                created_at=created_at
            )
            jobs.append(job)
        return jobs

    def create_applications(self, jobs, candidates):
        for job in jobs:
            num_apps = random.randint(1, MAX_APPS_PER_JOB)
            eligible_candidates = [c for c in candidates if c.last_education >= job.min_education]
            if not eligible_candidates:
                continue
            selected_candidates = random.sample(eligible_candidates, min(num_apps, len(eligible_candidates)))
            for candidate in selected_candidates:
                band_min, band_max = salary_bands[job.salary_band]
                salary = round(random.uniform(band_min, band_max), 2)
                created_at = job.created_at + timedelta(days=random.randint(0, 30))
                Application.objects.create(
                    job=job,
                    candidate=candidate,
                    salary_expectation=salary,
                    candidate_last_education=candidate.last_education,
                    candidate_experience=candidate.experience,
                    created_at=created_at
                )
