import json
import os

import numpy as np
import pickle

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt

from .models import PredictionHistory

model = pickle.load(open(os.path.join('blog', 'models', 'CarsModel.pkl'), 'rb'))


def predict_price(car_data):
    """Predict a car price from a dict of features.

    Accepts both long-form and short-form keys for mileage and engine size:
      - year
      - mileage  (alias: mil)
      - tax
      - mpg
      - engine_size (alias: es)

    The feature array is built in the SAME order as the home view:
    [year, mil, tax, mpg, es].

    Returns the rounded predicted price as a float (2 decimal places).
    Raises ValueError if a required feature is missing or cannot be
    converted to float.
    """
    # Normalize input keys, accepting both long-form and short-form aliases.
    year = car_data.get('year')
    mileage = car_data.get('mileage', car_data.get('mil'))
    tax = car_data.get('tax')
    mpg = car_data.get('mpg')
    engine_size = car_data.get('engine_size', car_data.get('es'))

    features = {
        'year': year,
        'mileage': mileage,
        'tax': tax,
        'mpg': mpg,
        'engine_size': engine_size,
    }

    # Validate presence and convertibility to float.
    converted = []
    for name, value in features.items():
        if value is None:
            raise ValueError(
                "Missing required feature: '{}'. Expected one of the keys "
                "year, mileage/mil, tax, mpg, engine_size/es.".format(name)
            )
        try:
            converted.append(float(value))
        except (TypeError, ValueError):
            raise ValueError(
                "Feature '{}' must be a number, got {!r}.".format(name, value)
            )

    # Build the feature array in the SAME order as the home view:
    # [year, mil, tax, mpg, es]
    arr = converted
    y_pred = model.predict(np.array([arr], dtype=float))
    return round(float(y_pred[0]), 2)


def home(request):
    if request.method == 'POST':
        car_data = {
            'year': request.POST.get('year'),
            'mil': request.POST.get('mil'),
            'tax': request.POST.get('tax'),
            'mpg': request.POST.get('mpg'),
            'es': request.POST.get('es'),
        }
        prediction = predict_price(car_data)
        return render(request, "home.html", {'result': int(round(prediction))})
    return render(request, 'home.html')


@csrf_exempt
def predict_api(request):
    """REST API endpoint for car price prediction.

    Accepts a POST request with a JSON body containing car features, e.g.:
        {"year": 2019, "mileage": 15000, "tax": 145, "mpg": 55.4, "engine_size": 1.5}

    Returns a JSON response with the predicted price. If the user is
    authenticated, the prediction is also saved to PredictionHistory.
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)

    try:
        data = json.loads(request.body)
    except (ValueError, TypeError) as e:
        return JsonResponse(
            {'error': 'Invalid JSON body: {}'.format(e)}, status=400
        )

    try:
        prediction = predict_price(data)
    except ValueError as e:
        return JsonResponse({'error': str(e)}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

    if request.user.is_authenticated:
        PredictionHistory.objects.create(
            user=request.user,
            car_model=data.get('car_model', 'Unknown'),
            predicted_price=prediction
        )

    return JsonResponse({'predicted_price': prediction})


def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not username or not email or not password:
            messages.error(request, 'All fields are required.')
            return render(request, 'register.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return render(request, 'register.html')

        user = User.objects.create_user(
            username=username, email=email, password=password
        )
        login(request, user)
        messages.success(request, 'Account created successfully.')
        return redirect('home')

    return render(request, 'register.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Logged in successfully.')
            return redirect('home')
        messages.error(request, 'Invalid username or password.')
        return render(request, 'login.html')

    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    messages.success(request, 'Logged out successfully.')
    return redirect('home')


@login_required
def user_history(request):
    history = PredictionHistory.objects.filter(user=request.user).order_by('-timestamp')
    return render(request, 'history.html', {'history': history})
