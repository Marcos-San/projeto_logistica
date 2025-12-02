from django.shortcuts import render
from .models import *
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import logout

def home(request):
    return render(request, 'log/home.html')

def index(request):
    return render(request, 'log/index.html')

def custom_logout(request):
    logout(request)
    return redirect('home')

def lista_motorista(request):
    motoristas = Motorista.objects.all()
    return render(request, 'log/lista_motorista.html')

