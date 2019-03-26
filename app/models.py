import datetime

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from app.static.app.sampledata import aikataulut

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Tähän profiilin parametrejä
    pysakki = models.CharField(max_length=50, default='Keskustori')

    def __str__(self):
        return self.user.username

class Stop(models.Model):
    id_2 = models.CharField(max_length=4, unique=True)
    name = models.TextField()


