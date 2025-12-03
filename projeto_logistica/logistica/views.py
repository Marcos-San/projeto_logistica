from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .forms import MotoristaForm
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
def list_motorista(request):
    motoristas = MotoristaForm()
    context = {
        'motorista': motoristas
    }
    return render(request, 'log/list_motorista.html')

@login_required()
def criar_motorista(request):
    form = MotoristaForm()
    context = {
        'form': form
    }
    return render(request, 'log/criar_motorista.html')
