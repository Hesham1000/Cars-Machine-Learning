from django.contrib.auth.models import User
from django.db import models


class Register(models.Model):
    username = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    password = models.CharField(max_length=50, unique=True, help_text='please enter password')

    def __str__(self):
        return self.username


class PredictionHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    car_model = models.CharField(max_length=100)
    predicted_price = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f'{self.car_model} - {self.predicted_price}'
