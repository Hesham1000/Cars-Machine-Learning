from cProfile import label
import email
from django.db import models
from django.contrib.auth.models import User
from numpy import require

class Register(models.Model):
    username = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    password = models.CharField(max_length=50, unique=True, help_text='please enter password')

class CarPrediction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='predictions')
    car_model = models.CharField(max_length=255)
    predicted_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']