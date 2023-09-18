from cProfile import label
import email
from django.db import models
from numpy import require

class Register(models.Model):
    username = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    password = models.CharField(max_length=50, unique=True, help_text='please enter password')