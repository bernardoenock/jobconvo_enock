from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as gl
from .managers import UserManager

class User(AbstractUser):
  username = None
  email = models.EmailField(gl('email address'), unique=True)
  
  is_company = models.BooleanField(default=False)
  is_candidate = models.BooleanField(default=False)

  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = []

  objects = UserManager()

  def __str__(self):
      return self.email

class Company(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='company')
  name = models.CharField(max_length=255)

  def __str__(self):
    return self.name

class Candidate(models.Model):
  class Education(models.IntegerChoices):
     FUNDAMENTAL = 1, 'Ensino fundamental'
     MEDIO = 2, 'Ensino médio'
     TECNOLOGO = 3, 'Tecnólogo'
     SUPERIOR = 4, 'Ensino superior'
     POS_MBA_MESTRADO = 5, 'Pós / MBA / Mestrado'
     DOUTORADO = 6, 'Doutorado'
  
  user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='candidate')
  last_education = models.IntegerField(choices=Education.choices, default=Education.MEDIO)
  experience = models.TextField(blank=True)

  def __str__(self):
    return self.user.email