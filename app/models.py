import datetime
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

class Profile(models.Model):
    valinnat = (
        (0, 0),
        (1, 1),
        (2, 2)
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Tähän profiilin parametrejä
    linja = models.CharField(max_length=5, default='3')
    pysakki = models.CharField(max_length=50, default='Itsenäisyydenkatu 10')

    def __str__(self):
        return self.user.username

class Stop(models.Model):
    id_2 = models.CharField(max_length=5, unique=True)
    name = models.TextField()


