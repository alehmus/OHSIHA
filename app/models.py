import datetime
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from app.static.app.sampledata import aikataulut

# Create your models here.

class Profile(models.Model):
    valinnat = (
        (0, 0),
        (1, 1),
        (2, 2)
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Tähän profiilin parametrejä
    pysakki1 = models.CharField(max_length=50, default='Itsenäisyydenkatu 10')
    pysakki2 = models.CharField(max_length=50, default='TTY')
    pysakki3 = models.CharField(max_length=50, default='Ahvenisjärvi')
    pysakkivalinta = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username

class Stop(models.Model):
    id_2 = models.CharField(max_length=5, unique=True)
    name = models.TextField()


