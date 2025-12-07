from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

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


# ========== CRUD MOTORISTA ==========
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
            messages.success(request, 'Motorista cadastrado com sucesso!')
        }

        return redirect('list_motorista')


@login_required()
def atualizar_motorista(request, id):
    motorista = get_object_or_404(Motorista, id=id)

    if request.method == 'POST':
        form = MotoristaForm(request.POST, instance=motorista)

        if form.is_valid():
            form.save()
            messages.success(request, 'Dados atualizados com sucesso!')
            return redirect('list_motorista')  # ajuste para a URL correta
    else:
        # GET → mostra o formulário com dados carregados
        form = MotoristaForm(instance=motorista)

    context = {
        'form': form
    }
    return render(request, 'log/atualizar_motorista.html', context)

@login_required()
def deletar_motorista(request, id):
    motorista = get_object_or_404(Motorista, id=id)
    motorista.delete()
    messages.success(request, 'Motorista deletado com sucesso!')
    return redirect('list_motorista')