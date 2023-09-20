from msilib.schema import ListView
from multiprocessing import context
import numpy as np
from pyexpat import model
from re import template
from turtle import title
from django.shortcuts import render
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

# def login(request):
#     r1 = request.POST.get('name')
#     r2 = request.POST.get('email')
#     r3 = request.POST.get('password')
#     data = Register(username = r1, email = r2, password = r3) 
#     if request.method == 'POST':
#         data.save()     
#     return render(request, 'login.html')




