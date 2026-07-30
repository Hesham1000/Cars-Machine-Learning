from msilib.schema import ListView
from multiprocessing import context
import numpy as np
from pyexpat import model
from re import template
from turtle import title
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.conf import settings
import blog
from .models import Register
import pickle
import json
import stripe

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


@require_POST
def reserve_car(request):
    try:
        data = json.loads(request.body)
        car_id = data.get('car_id')

        stripe.api_key = settings.STRIPE_SECRET_KEY

        session = stripe.checkout.Session.create(
            mode='payment',
            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': 'Car Reservation',
                        },
                        'unit_amount': 1000,
                    },
                    'quantity': 1,
                },
            ],
            success_url='http://localhost:8000/success/?session_id={CHECKOUT_SESSION_ID}',
            cancel_url='http://localhost:8000/cancel/',
        )

        return JsonResponse({'checkout_url': session.url})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)






