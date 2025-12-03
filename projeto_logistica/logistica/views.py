from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import *
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import logout

def home(request):
    return render(request, 'log/home.html')

def custom_logout(request):
    logout(request)
    return redirect('home')

@login_required()
def lista_motorista(request):
    motoristas = Motorista.objects.all()
    return render(request, 'log/lista_motorista.html')

