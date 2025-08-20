from django.db import models
from django.conf import settings
from django.utils import timezone
from accounts.models import Company, Candidate

class Job(models.Model):
  class SalaryBand(models.IntegerChoices):
    UP_TO_1K = 1, 'Até R$ 1.000'
    FROM_1K_TO_2K = 2, 'De 1.000 até R$ 2.000'
    FROM_2K_TO_3K = 3, 'De 2.000 até R$ 3.000'
    ABOVE_3K = 4, 'Acima de R$ 3.000'

  class MinEducation(models.IntegerChoices):
    FUNDAMENTAL = 1, 'Ensino fundamental'
    MEDIO = 2, 'Ensino médio'
    TECNOLOGO = 3, 'Tecnólogo'
    SUPERIOR = 4, 'Ensino superior'
    POS_MBA_MESTRADO = 5, 'Pós / MBA / Mestrado'
    DOUTORADO = 6, 'Doutorado'

  company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='jobs')
  title = models.CharField(max_length=255)
  salary_band = models.IntegerField(choices=SalaryBand.choices)
  requirements = models.TextField()
  min_education = models.IntegerField(choices=MinEducation.choices)
  created_at = models.DateTimeField(default=timezone.now)

  def __str__(self):
    return f'{self.title} @ {self.company}'
  
  @property
  def applications_count(self):
    return self.applications_count()

class Application(models.Model):
  job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
  candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='applications')

  salary_expectation = models.DecimalField(max_digits=10, decimal_places=2)
  candidate_last_education = models.IntegerField(choices=Job.MinEducation.choices)
  candidate_experience = models.TextField(blank=True)

  score = models.PositiveSmallIntegerField(default=0)
  created_at = models.DateTimeField(default=timezone.now)

  class Meta:
    unique_together = ('job', 'candidate')

  def __str__(self):
    return f'{self.candidate} -> {self.job}'
  
  def compute_score(self):
    score = 0

    if self._salary_fits_band():
      score += 1

    if self.candidate_last_education >= self.job.min_education:
      score += 1
    
    return score
  
  def _salary_fits_band(self):
    s = float(self.salary_expectation)
    band = self.job.salary_band

    salary_map = {
        Job.SalaryBand.UP_TO_1K: lambda val: val <= 1000,
        Job.SalaryBand.FROM_1K_TO_2K: lambda val: 1000 <= val <= 2000,
        Job.SalaryBand.FROM_2K_TO_3K: lambda val: 2000 <= val <= 3000,
        Job.SalaryBand.ABOVE_3K: lambda val: val > 3000,
    }

    return salary_map.get(band, lambda val: False)(s)
  
  def save(self, *args, **kwargs):
    self.score = self.compute_score()
    super().save(*args, **kwargs)
