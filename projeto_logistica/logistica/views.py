from django.shortcuts import render
from .models import *
from django.shortcuts import render, redirect
from django.http import HttpResponse


def home(request):
    return render(request, 'log/home.html')


def lista_motorista(request):
    motoristas = Motorista.objects.all()
    return render(request, 'log/lista_motorista.html')

