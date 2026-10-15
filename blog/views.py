import os
import pickle
import json
import random

import numpy as np
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout, User
from django.contrib import messages

from .models import Register, CarPrediction

# Load the trained model lazily so a missing/corrupt pickle file does not
# crash the whole app at import time (which would break migrations).
_model = None


def _get_model():
    global _model
    if _model is None:
        model_path = os.path.join(os.path.dirname(__file__), 'models', 'CarsModel.pkl')
        with open(model_path, 'rb') as fh:
            _model = pickle.load(fh)
    return _model


def home(request):
    if request.method == 'POST':
        year = request.POST['year']
        mil = request.POST['mil']
        tax = request.POST['tax']
        mpg = request.POST['mpg']
        es = request.POST['es'] 
        
        arr = [year, mil, tax, mpg, es]
        y_pred = _get_model().predict(np.array([arr], dtype=float))
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

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Logged in successfully')
            return redirect('home')
        else:
            messages.error(request, 'Invalid credentials')
    return render(request, 'login.html')

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
        else:
            User.objects.create_user(username=username, password=password)
            messages.success(request, 'Registration successful. Please login.')
            return redirect('login')
    return render(request, 'register.html')

@require_POST
@login_required
def predict_price(request):
    try:
        data = json.loads(request.body)
        car_model = data.get('car_model', 'Unknown')
        # Mock prediction logic: random price between 10000 and 100000
        price = random.uniform(10000, 100000)
        
        # Save to history
        CarPrediction.objects.create(
            user=request.user,
            car_model=car_model,
            predicted_price=price
        )
        
        return JsonResponse({'price': price, 'car_model': car_model})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@login_required
def user_history(request):
    predictions = CarPrediction.objects.filter(user=request.user)
    return render(request, 'history.html', {'predictions': predictions})
