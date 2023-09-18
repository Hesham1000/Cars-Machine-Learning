from distutils.command.upload import upload
from datetime import datetime
from django.db import models

class Car(models.Model):
    b=[
        ('BMW','BMW'),
        ('Toyota','Toyota'),
        ('Ford','Ford'),
        ('Honda', 'Honda'),
        ('Nissan','Nissan'),
        ('Audi','Audi'),
        ('Lamborghini','Lamborghini'),
        ('Volkswagen','Volkswagen'),
        ('Mercedes','Mercedes'),
    ]
    id = models.IntegerField(auto_created=True, primary_key=True, verbose_name='ID')
    name = models.CharField(max_length=50, verbose_name='Name')
    price = models.CharField(max_length=20, verbose_name='Price')
    brand = models.CharField(max_length=50, null=True, blank=True, choices=b, verbose_name='Brand')
    image = models.ImageField(upload_to='photos/%y/%m/%d', verbose_name='Photo')
    date_time = models.DateTimeField(default= datetime.now, verbose_name='Date_Time')
    active = models.BooleanField(default=True, verbose_name='Active')
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['id']
    
