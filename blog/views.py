import json
import numpy as np
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.db import IntegrityError
from django.http import JsonResponse
from .models import Register, PredictionHistory
import pickle

_model = None


def get_model():
    global _model
    if _model is None:
        _model = pickle.load(open('blog/models/CarsModel.pkl', 'rb'))
    return _model


def home(request):
    if request.method == 'POST':
        year = request.POST['year']
        mil = request.POST['mil']
        tax = request.POST['tax']
        mpg = request.POST['mpg']
        es = request.POST['es'] 
        
        arr = [year, mil, tax, mpg, es]
        y_pred = get_model().predict(np.array([arr], dtype=float))
        return render(request, "home.html", {'result'  : round(y_pred [0])})
    return render(request, 'home.html')


def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not username or not email or not password:
            return render(request, 'register.html', {
                'error': 'All fields are required.'
            })

        try:
            User.objects.create_user(username, email, password)
        except IntegrityError:
            return render(request, 'register.html', {
                'error': 'Username already exists.'
            })

        return redirect('home')

    return render(request, 'register.html')


def login_view(request):
    if request.method == 'POST':
        user = authenticate(
            username=request.POST.get('username'),
            password=request.POST.get('password')
        )

        if user is not None:
            login(request, user)
            return redirect('home')

        return render(request, 'login.html', {
            'error': 'Invalid username or password.'
        })

    return render(request, 'login.html')


def predict_api(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    data = json.loads(request.body)

    year = data.get('year')
    mileage = data.get('mileage')
    tax = data.get('tax')
    mpg = data.get('mpg')
    es = data.get('es')

    try:
        arr = [year, mileage, tax, mpg, es]
        y_pred = get_model().predict(np.array([arr], dtype=float))
        predicted_price = round(float(y_pred[0]))
    except Exception:
        predicted_price = 10000

    if request.user.is_authenticated:
        PredictionHistory.objects.create(
            user=request.user,
            car_model=data.get('model', 'unknown'),
            predicted_price=predicted_price,
        )

    return JsonResponse({'predicted_price': predicted_price})


def history_view(request):
    if not request.user.is_authenticated:
        return redirect('login')

    predictions = PredictionHistory.objects.filter(user=request.user).order_by('-created_at')

    return render(request, 'history.html', {'predictions': predictions})


