from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('api/predict/', views.predict_price, name='predict'),
    path('history/', views.user_history, name='history'),
]
