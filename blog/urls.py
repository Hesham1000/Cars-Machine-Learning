from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('api/reserve-car/', views.reserve_car, name='reserve_car'),
    # path('login/', views.login, name='login'),
]

