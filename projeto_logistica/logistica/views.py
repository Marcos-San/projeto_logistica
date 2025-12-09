from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

from .forms import *
from .models import *
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import logout

def home(request):
    return render(request, 'log/home.html')

def custom_logout(request):
    logout(request)
    return redirect('home')

def buscar_entrega(request):
    buscar = request.GET.get('pesquisa')

    if buscar:
        try:
            resultado = Entrega.objects.get(codigo_rastreio=buscar)
        except (ValueError, Entrega.DoesNotExist):
            resultado = None
        context = {
            'resultado': resultado,
            'buscar': buscar,
        }

    return render(request, 'log/buscar_entrega.html', context)



# ========== CRUD MOTORISTA ==========
@login_required()
def list_motorista(request):
    motoristas = Motorista.objects.all()
    return render(request, 'log/list_motorista.html', {'motoristas': motoristas})

@login_required()
def criar_motorista(request):
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
            return redirect('list_motorista')
    else:
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



# ========== CRUD CLIENTE ==========
@login_required()
def list_cliente(request):
    clientes = Cliente.objects.all()
    return render(request, 'log/list_cliente.html', {'clientes': clientes})

@login_required()
def criar_cliente(request):
    if request.method == 'GET':
        form = ClienteForm()
        context = {
            'form' : form
        }
        return render(request, 'log/criar_cliente.html', context)
    else:
        form = ClienteForm(request.POST)
        if form.is_valid():
            new = Cliente()
            new.nome = form['nome'].value()
            new.email = form['email'].value()
            new.telefone = form['telefone'].value()

            new.save()
        context = {
            messages.success(request, 'Cliente cadastrado com sucesso!')
        }

        return redirect('list_cliente')


@login_required()
def atualizar_cliente(request, id):
    cliente = get_object_or_404(Cliente, id=id)

    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)

        if form.is_valid():
            form.save()
            messages.success(request, 'Dados atualizados com sucesso!')
            return redirect('list_cliente')
    else:
        form = ClienteForm(instance=cliente)

    context = {
        'form': form
    }
    return render(request, 'log/atualizar_cliente.html', context)

@login_required()
def deletar_cliente(request, id):
    cliente = get_object_or_404(Cliente, id=id)
    cliente.delete()
    messages.success(request, 'Cliente deletado com sucesso!')
    return redirect('list_cliente')



# ========== CRUD VEICULO ==========
@login_required()
def list_veiculo(request):
    veiculos =  Veiculo.objects.all()
    return render(request, 'log/list_veiculo.html', {'veiculos': veiculos})

@login_required()
def criar_veiculo(request):
    if request.method == 'GET':
        form = VeiculoForm()
        context = {
            'form' : form
        }
        return render(request, 'log/criar_veiculo.html', context)
    else:
        form = VeiculoForm(request.POST)
        if form.is_valid():
            form.save()

        context = {
            messages.success(request, 'Veiculo cadastrado com sucesso!')
        }

        return redirect('list_veiculo')


@login_required()
def atualizar_veiculo(request, id):
    veiculo = get_object_or_404(Veiculo, id=id)

    if request.method == 'POST':
        form = VeiculoForm(request.POST, instance=veiculo)

        if form.is_valid():
            form.save()
            messages.success(request, 'Dados atualizados com sucesso!')
            return redirect('list_veiculo')
    else:
        form = VeiculoForm(instance=veiculo)

    context = {
        'form': form
    }
    return render(request, 'log/atualizar_veiculo.html', context)

@login_required()
def deletar_veiculo(request, id):
    veiculo = get_object_or_404(Veiculo, id=id)
    veiculo.delete()
    messages.success(request, 'Veiculo deletado com sucesso!')
    return redirect('list_veiculo')



# ========== CRUD ENTREGA ==========
@login_required()
def list_entrega(request):
    entregas = Entrega.objects.all()
    return render(request, 'log/list_entrega.html', {'entregas': entregas})

@login_required()
def criar_entrega(request):
    if request.method == 'GET':
        form = EntregaForm()
        context = {
            'form' : form
        }
        return render(request, 'log/criar_entrega.html', context)
    else:
        form = EntregaForm(request.POST)
        if form.is_valid():
            form.save()

        context = {
            messages.success(request, 'Entrega registrada com sucesso!')
        }

        return redirect('list_entrega')


@login_required()
def atualizar_entrega(request, id):
    entrega = get_object_or_404(Entrega, id=id)

    if request.method == 'POST':
        form = EntregaForm(request.POST, instance=entrega)

        if form.is_valid():
            form.save()
            messages.success(request, 'Dados atualizados com sucesso!')
            return redirect('list_entrega')
    else:
        form = EntregaForm(instance=entrega)

    context = {
        'form': form
    }
    return render(request, 'log/atualizar_entrega.html', context)

@login_required()
def deletar_entrega(request, id):
    entrega = get_object_or_404(Entrega, id=id)
    entrega.delete()
    messages.success(request, 'Entrega deletado com sucesso!')
    return redirect('list_entrega')