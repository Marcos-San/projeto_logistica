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
        context = {
            'form' : form
        }
        return render(request, 'log/criar_motorista.html', context)
    else:
        form = MotoristaForm(request.POST)
        if form.is_valid():
            new = Motorista()
            new.nome = form['nome'].value()
            new.cpf = form['cpf'].value()
            new.cnh = form['cnh'].value()
            new.telefone = form['telefone'].value()
            new.status = form.cleaned_data['status']
            new.data_cadastro = form['data_cadastro'].value()

            new.save()
        context = {
            'form': form,
            'mensagem' : "Motorista cadastrado com sucesso!"
        }

        return render(request, 'log/criar_motorista.html', context=context)