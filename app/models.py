import datetime
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Profiilin 'ylimääräiset' parametrit
    linja = models.CharField(max_length=5, default='3')
    pysakki = models.CharField(max_length=50, default='Itsenäisyydenkatu 10')

    def __str__(self):
        return self.user.username

class Stop(models.Model):
    # pysäkkiluokan ominaisuudet
    id_2 = models.CharField(max_length=5, unique=True)
    name = models.TextField()


