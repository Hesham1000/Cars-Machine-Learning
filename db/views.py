from django.shortcuts import render
from .models import Car


def Cars(request):
    return render(request, 'sqlite.html', {'c': Car.objects.all()})

