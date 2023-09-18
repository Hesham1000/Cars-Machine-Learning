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
# lb = pickle.load(open('blog\models\CarsModelLE.pkl', 'rb'))


def home(request):
    if request.method == 'POST':
        year = request.POST['year']
        # trans = request.POST['trans']
        mil = request.POST['mil']
        # ft = request.POST['ft']
        tax = request.POST['tax']
        mpg = request.POST['mpg']
        es = request.POST['es'] 
        # ei = request.POST['ei']
        # ni = request.POST['ni']
        # te = request.POST['te']
        # el = request.POST['el']
        # tw = request.POST['tw']
        
        # trans = lb.transform([trans])
        # ft = lb.transform([ft])
        
        arr = [year, mil, tax, mpg, es]
        y_pred = model.predict(np.array([arr], dtype=float))
        return render(request, "home.html", {'result'  : round(y_pred [0])})
    return render(request, 'home.html')

def login(request):
    r1 = request.POST.get('name')
    r2 = request.POST.get('email')
    r3 = request.POST.get('password')
    data = Register(username = r1, email = r2, password = r3) 
    if request.method == 'POST':
        data.save()     
    return render(request, 'login.html')

def sqlite(request):
    return render(request, 'sqlite.html')

# def forminfo(request):
    
#     return render(request, 'result.html')
    
    
# class S(ListView):
    # model = blog
    # template_name = 'sqlite.html'    
    # context_object_name = 'posts'
    
    
# def get_queryset(self):
    # query = self.request.GET.get('c')
    # return blog.objects.filter(title_icon=query).order_by('-created_at')
