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
    motoristas = Motorista.objects.all()
    return render(request, 'log/list_motorista.html', {'motoristas': motoristas})

@login_required()
def criar_motorista(request):
    context = {}
    if request.method == 'GET':
        form = MotoristaForm()
        context['form'] = MotoristaForm()
        return render(request, 'log/criar_motorista.html', context)
    elif request.method == 'POST' and request.FILES != None:
        form = MotoristaForm(request.POST, request.FILES)
        if form.is_valid():
            new = Motorista()
            new.nome = form['nome'].value()
            new.cpf = form['cpf'].value()
            new.cnh = form['cnh'].value()
            new.telefone = form['telefone'].value()
            new.status = form['status'].value
            new.data_cadastro = form['data_cadastro'].value()

            new.save()
            return redirect('log/list_motorista.html')
