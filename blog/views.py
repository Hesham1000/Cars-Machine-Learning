from msilib.schema import ListView
from multiprocessing import context
import numpy as np
from pyexpat import model
from re import template
from turtle import title
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
import blog
from .models import Register
import pickle

model = pickle.load(open('blog\models\CarsModel.pkl', 'rb'))


def home(request):
    if request.method == 'POST':
        year = request.POST['year']
        mil = request.POST['mil']
        tax = request.POST['tax']
        mpg = request.POST['mpg']
        es = request.POST['es'] 
        
        arr = [year, mil, tax, mpg, es]
        y_pred = model.predict(np.array([arr], dtype=float))
        return render(request, "home.html", {'result'  : round(y_pred [0])})
    return render(request, 'home.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    return render(request, 'login.html')


def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            login(request, user)
            return redirect('home')
        except Exception as e:
            return render(request, 'login.html', {'error': str(e)})
    return render(request, 'login.html')






