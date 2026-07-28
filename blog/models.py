from cProfile import label
import email
from django.db import models
from numpy import require

class Register(models.Model):
    username = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    password = models.CharField(max_length=50, unique=True, help_text='please enter password')


class CarBrand(models.Model):
    name = models.CharField(max_length=100)
    logo = models.URLField(max_length=500)
    country = models.CharField(max_length=50)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
