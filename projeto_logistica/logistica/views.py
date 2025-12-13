from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404
from django.contrib.auth import logout
from django.db.models import Q, Sum
from .forms import MotoristaForm, ClienteForm, VeiculoForm, EntregaForm, RotaForm, GerenciarAcessoMotoristaForm, \
    CriarUsuarioMotoristaForm
from .models import Motorista, Cliente, Veiculo, Entrega, Rota
from .permissions import *  # Importe as novas funções de permissão



# HOME E AUTENTICAÇÃO -------------------------------------

def home(request):
    """Dashboard principal com estatísticas - Acesso público"""
    # Para usuários não autenticados, mostrar apenas busca
    if not request.user.is_authenticated:
        return render(request, 'log/home.html', {})

    # Para usuários autenticados, mostrar dashboard apropriado
    if request.user.is_staff:
        # Admin vê todas as estatísticas
        context = {
            'total_entregas': Entrega.objects.count(),
            'entregas_pendentes': Entrega.objects.filter(status='pendente').count(),
            'entregas_em_transito': Entrega.objects.filter(status='em_transito').count(),
            'entregas_entregues': Entrega.objects.filter(status='entregue').count(),
            'entregas_sem_rota': Entrega.objects.filter(rota__isnull=True).count(),
            'total_motoristas': Motorista.objects.count(),
            'motoristas_disponiveis': Motorista.objects.filter(status='disponivel').count(),
            'total_veiculos': Veiculo.objects.count(),
            'veiculos_disponiveis': Veiculo.objects.filter(status='disponivel').count(),
            'rotas_ativas': Rota.objects.filter(status='em_andamento').count(),
            'entregas_recentes': Entrega.objects.all().select_related('cliente', 'motorista', 'rota').order_by(
                '-data_solicitacao')[:10],
        }
    elif hasattr(request.user, 'motorista'):
        # Motorista vê apenas suas estatísticas
        motorista = request.user.motorista
        context = {
            'total_entregas': Entrega.objects.filter(motorista=motorista).count(),
            'entregas_pendentes': Entrega.objects.filter(motorista=motorista, status='pendente').count(),
            'entregas_em_transito': Entrega.objects.filter(motorista=motorista, status='em_transito').count(),
            'entregas_entregues': Entrega.objects.filter(motorista=motorista, status='entregue').count(),
            'entregas_sem_rota': Entrega.objects.filter(motorista=motorista, rota__isnull=True).count(),
            'total_motoristas': 1,  # Apenas ele mesmo
            'motoristas_disponiveis': 1 if motorista.status == 'disponivel' else 0,
            'total_veiculos': Veiculo.objects.filter(motorista=motorista).count(),
            'veiculos_disponiveis': Veiculo.objects.filter(motorista=motorista, status='disponivel').count(),
            'rotas_ativas': Rota.objects.filter(motorista=motorista, status='em_andamento').count(),
            'entregas_recentes': Entrega.objects.filter(motorista=motorista).select_related('cliente', 'motorista',
                                                                                            'rota').order_by(
                '-data_solicitacao')[:10],
        }
    else:
        # Usuário comum autenticado (sem perfil específico)
        context = {
            'total_entregas': 0,
            'entregas_pendentes': 0,
            'entregas_em_transito': 0,
            'entregas_entregues': 0,
            'entregas_sem_rota': 0,
            'total_motoristas': 0,
            'motoristas_disponiveis': 0,
            'total_veiculos': 0,
            'veiculos_disponiveis': 0,
            'rotas_ativas': 0,
            'entregas_recentes': [],
        }
        messages.info(request, 'Você não tem um perfil específico. Contate o administrador para mais acesso.')

    return render(request, 'log/home.html', context)


def custom_logout(request):
    """Logout customizado - Acesso público"""
    logout(request)
    messages.success(request, 'Logout realizado com sucesso!')
    return redirect('home')


def buscar_entrega(request):
    """Busca entrega por código de rastreio - Acesso público"""
    buscar = request.GET.get('pesquisa')
    resultado = None

    if buscar:
        try:
            resultado = Entrega.objects.select_related('cliente', 'motorista', 'rota').get(codigo_rastreio=buscar)
        except Entrega.DoesNotExist:
            messages.error(request, f'Entrega "{buscar}" não encontrada!')
        except Exception as e:
            messages.error(request, f'Erro ao buscar entrega: {str(e)}')

    context = {
        'resultado': resultado,
        'buscar': buscar,
    }
    return render(request, 'log/buscar_entrega.html', context)


# CRUD MOTORISTA -------------------------------------

@login_required
@user_passes_test(lambda u: u.is_staff)
def list_motorista(request):
    """Lista todos os motoristas com informações de acesso"""
    motoristas = Motorista.objects.all().order_by('nome')

    # Adicionar informações de acesso
    for motorista in motoristas:
        motorista.tem_acesso = motorista.user is not None
        motorista.acesso_ativo = motorista.user.is_active if motorista.user else False

    context = {
        'motoristas': motoristas,
        'total': motoristas.count(),
        'total_com_acesso': sum(1 for m in motoristas if m.tem_acesso),
        'total_ativos': sum(1 for m in motoristas if m.acesso_ativo),
    }
    return render(request, 'log/list_motorista.html', context)


@login_required
@user_passes_test(can_edit_motoristas, login_url='/login/')
@login_required
@user_passes_test(lambda u: u.is_staff)
@login_required
@user_passes_test(lambda u: u.is_staff)
def criar_motorista(request):
    """Criar novo motorista com usuário de acesso"""
    senha_gerada = None
    form = MotoristaForm()

    if request.method == 'POST':
        form = MotoristaForm(request.POST)
        if form.is_valid():
            try:
                motorista = form.save()

                # Verificar se foi gerada senha inicial
                if hasattr(form, 'senha_gerada'):
                    senha_gerada = form.senha_gerada

                    # GARANTIR que o usuário está no grupo Motoristas
                    if motorista.user:
                        motorista.adicionar_ao_grupo_motoristas()

                        # Verificar permissões
                        grupo_motorista = Group.objects.get(name='Motoristas')
                        permissoes_count = grupo_motorista.permissions.count()

                        messages.success(
                            request,
                            f'✅ Motorista cadastrado com sucesso!<br>'
                            f'<strong>Usuário:</strong> {motorista.user.username}<br>'
                            f'<strong>Senha:</strong> {senha_gerada}<br>'
                            f'<strong>Grupo:</strong> Motoristas ({permissoes_count} permissões)'
                        )
                    else:
                        messages.success(request, 'Motorista cadastrado, mas usuário não foi criado.')
                else:
                    messages.success(request, 'Motorista cadastrado com sucesso!')

                return redirect('list_motorista')

            except Exception as e:
                messages.error(request, f'Erro ao salvar motorista: {str(e)}')
        else:
            messages.error(request, 'Erro ao cadastrar motorista. Verifique os dados.')

    # Renderizar o formulário
    context = {
        'form': form,
        'senha_gerada': senha_gerada
    }
    return render(request, 'log/criar_motorista.html', context)


@login_required
def detalhes_motorista(request, id):
    """Detalhes do motorista com informações de acesso"""
    motorista = get_object_or_404(Motorista, id=id)

    # Verificar permissão
    if not (request.user.is_staff or
            (hasattr(request.user, 'motorista_profile') and
             request.user.motorista_profile.id == motorista.id)):
        messages.error(request, 'Acesso negado.')
        return redirect('home')

    # Estatísticas do motorista
    entregas = Entrega.objects.filter(motorista=motorista)
    rotas = Rota.objects.filter(motorista=motorista)

    context = {
        'motorista': motorista,
        'total_entregas': entregas.count(),
        'entregas_pendentes': entregas.filter(status='pendente').count(),
        'entregas_entregues': entregas.filter(status='entregue').count(),
        'rotas_ativas': rotas.filter(status='em_andamento').count(),
        'rotas_concluidas': rotas.filter(status='concluida').count(),
    }

    return render(request, 'log/detalhes_motorista.html', context)


@login_required
@user_passes_test(lambda u: u.is_staff)
def gerenciar_acesso_motorista(request, id):
    """Gerenciar acesso do motorista ao sistema"""
    motorista = get_object_or_404(Motorista, id=id)

    if request.method == 'POST':
        form = GerenciarAcessoMotoristaForm(request.POST)
        if form.is_valid():
            acao = form.cleaned_data['acao']
            email = form.cleaned_data['email_credenciais']

            if acao == 'resetar_senha':
                if motorista.user:
                    nova_senha = motorista.resetar_senha()
                    messages.success(
                        request,
                        f'Senha resetada! Nova senha: <strong>{nova_senha}</strong>'
                    )

                    # Enviar email com nova senha
                    if email:
                        try:
                            send_mail(
                                'Nova Senha - LogiTrans',
                                f'Olá {motorista.nome},\n\n'
                                f'Sua senha foi redefinida.\n'
                                f'Nova senha: {nova_senha}\n\n'
                                f'Acesse: {request.build_absolute_uri("/")}\n'
                                f'Recomendamos alterar sua senha no primeiro acesso.\n\n'
                                f'Atenciosamente,\nEquipe LogiTrans',
                                settings.DEFAULT_FROM_EMAIL,
                                [email],
                                fail_silently=True,
                            )
                            messages.info(request, f'Nova senha enviada para: {email}')
                        except Exception as e:
                            messages.warning(request, f'Email não pôde ser enviado: {str(e)}')
                else:
                    messages.error(request, 'Motorista não possui usuário cadastrado.')

            elif acao == 'bloquear_acesso':
                if motorista.bloquear_acesso():
                    messages.success(request, 'Acesso bloqueado com sucesso!')
                else:
                    messages.error(request, 'Erro ao bloquear acesso.')

            elif acao == 'liberar_acesso':
                if motorista.liberar_acesso():
                    messages.success(request, 'Acesso liberado com sucesso!')
                else:
                    messages.error(request, 'Erro ao liberar acesso.')

            elif acao == 'reenviar_credenciais':
                if motorista.user:
                    # Gerar senha temporária
                    import random
                    import string
                    senha_temp = ''.join(random.choices(string.digits, k=4)) + '@Motorista'
                    motorista.user.set_password(senha_temp)
                    motorista.user.save()

                    # Enviar email
                    email_destino = email or motorista.user.email
                    if email_destino:
                        try:
                            send_mail(
                                'Credenciais de Acesso - LogiTrans',
                                f'Olá {motorista.nome},\n\n'
                                f'Suas credenciais de acesso:\n'
                                f'Usuário: {motorista.user.username}\n'
                                f'Senha: {senha_temp}\n\n'
                                f'Acesse: {request.build_absolute_uri("/")}\n'
                                f'Recomendamos alterar sua senha no primeiro acesso.\n\n'
                                f'Atenciosamente,\nEquipe LogiTrans',
                                settings.DEFAULT_FROM_EMAIL,
                                [email_destino],
                                fail_silently=True,
                            )
                            messages.success(request, f'Credenciais enviadas para: {email_destino}')
                        except Exception as e:
                            messages.error(request, f'Erro ao enviar email: {str(e)}')
                    else:
                        messages.warning(request, 'Nenhum email cadastrado para envio.')
                else:
                    messages.error(request, 'Motorista não possui usuário cadastrado.')

            return redirect('gerenciar_acesso_motorista', id=id)
    else:
        form = GerenciarAcessoMotoristaForm()

    form_criar_usuario = CriarUsuarioMotoristaForm()

    context = {
        'motorista': motorista,
        'form': form,
        'form_criar_usuario': form_criar_usuario,
    }
    return render(request, 'log/gerenciar_acesso_motorista.html', context)


@login_required
@user_passes_test(lambda u: u.is_staff)
def criar_usuario_motorista(request, id):
    """Criar usuário para motorista existente"""
    motorista = get_object_or_404(Motorista, id=id)

    if motorista.user:
        messages.error(request, 'Este motorista já possui usuário cadastrado.')
        return redirect('gerenciar_acesso_motorista', id=id)

    if request.method == 'POST':
        form = CriarUsuarioMotoristaForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            enviar_email = form.cleaned_data.get('enviar_email')

            # Criar usuário
            user, senha_gerada = motorista.criar_usuario()

            # Atualizar email se fornecido
            if email:
                user.email = email
                user.save()

            messages.success(
                request,
                f'Usuário criado com sucesso! '
                f'Usuário: <strong>{user.username}</strong> | '
                f'Senha: <strong>{senha_gerada}</strong>'
            )

            # Enviar email se solicitado
            if enviar_email:
                email_destino = email or user.email
                if email_destino:
                    try:
                        send_mail(
                            'Credenciais de Acesso - LogiTrans',
                            f'Olá {motorista.nome},\n\n'
                            f'Sua conta no sistema LogiTrans foi criada.\n'
                            f'Usuário: {user.username}\n'
                            f'Senha: {senha_gerada}\n\n'
                            f'Acesse: {request.build_absolute_uri("/")}\n'
                            f'Recomendamos alterar sua senha no primeiro acesso.\n\n'
                            f'Atenciosamente,\nEquipe LogiTrans',
                            settings.DEFAULT_FROM_EMAIL,
                            [email_destino],
                            fail_silently=True,
                        )
                        messages.info(request, f'Credenciais enviadas para: {email_destino}')
                    except Exception as e:
                        messages.warning(request, f'Email não pôde ser enviado: {str(e)}')

            return redirect('gerenciar_acesso_motorista', id=id)
    else:
        form = CriarUsuarioMotoristaForm()

    context = {
        'motorista': motorista,
        'form': form,
    }
    return render(request, 'log/criar_usuario_motorista.html', context)


@login_required
@user_passes_test(lambda u: u.is_staff)
def verificar_grupos_motoristas(request):
    """Verifica e corrige os grupos dos motoristas"""
    from django.contrib.auth.models import Group

    try:
        # Criar/obter grupo Motoristas
        grupo_motorista, created = Group.objects.get_or_create(name='Motoristas')

        if created:
            messages.info(request, 'Grupo Motoristas criado automaticamente.')

        # Contadores
        motoristas_com_usuario = Motorista.objects.filter(user__isnull=False)
        motoristas_no_grupo = 0
        motoristas_adicionados = 0

        # Verificar cada motorista
        for motorista in motoristas_com_usuario:
            if grupo_motorista in motorista.user.groups.all():
                motoristas_no_grupo += 1
            else:
                # Adicionar ao grupo
                motorista.user.groups.add(grupo_motorista)
                motorista.user.save()
                motoristas_adicionados += 1

        messages.success(
            request,
            f'✅ Verificação concluída:<br>'
            f'• Motoristas com usuário: {motoristas_com_usuario.count()}<br>'
            f'• Já no grupo Motoristas: {motoristas_no_grupo}<br>'
            f'• Adicionados ao grupo: {motoristas_adicionados}<br>'
            f'• Total no grupo agora: {grupo_motorista.user_set.count()}'
        )

    except Exception as e:
        messages.error(request, f'Erro ao verificar grupos: {str(e)}')

    return redirect('list_motorista')


@login_required
def atualizar_motorista(request, id):
    """Atualizar motorista existente - Admin ou próprio motorista"""
    motorista = get_object_or_404(Motorista, id=id)

    # Verificar permissão
    if not can_edit_motorista(request.user, motorista):
        messages.error(request, 'Acesso negado. Você não tem permissão para editar este motorista.')
        return redirect('home')

    if request.method == 'POST':
        form = MotoristaForm(request.POST, instance=motorista)
        if form.is_valid():
            form.save()
            messages.success(request, 'Dados do motorista atualizados com sucesso!')

            # Redirecionar conforme perfil
            if request.user.is_staff:
                return redirect('list_motorista')
            else:
                return redirect('detalhes_motorista', id=motorista.id)
        else:
            messages.error(request, 'Erro ao atualizar motorista.')
    else:
        form = MotoristaForm(instance=motorista)

    context = {
        'form': form,
        'motorista': motorista,
    }
    return render(request, 'log/atualizar_motorista.html', context)


@login_required
@user_passes_test(can_edit_motoristas, login_url='/login/')
def deletar_motorista(request, id):
    """Deletar motorista - Apenas admin"""
    if not request.user.is_staff:
        messages.error(request, 'Acesso negado. Apenas administradores podem deletar motoristas.')
        return redirect('home')

    motorista = get_object_or_404(Motorista, id=id)
    nome = motorista.nome
    motorista.delete()
    messages.success(request, f'Motorista "{nome}" deletado com sucesso!')
    return redirect('list_motorista')


# CRUD CLIENTE -------------------------------------

@login_required
@user_passes_test(can_view_clientes, login_url='/login/')
def list_cliente(request):
    """Lista todos os clientes - Admin ou motorista"""
    clientes = Cliente.objects.all().order_by('nome')
    context = {
        'clientes': clientes,
        'total': clientes.count(),
    }
    return render(request, 'log/list_cliente.html', context)


@login_required
@user_passes_test(can_edit_clientes, login_url='/login/')
def criar_cliente(request):
    """Criar novo cliente - Apenas admin"""
    if not request.user.is_staff:
        messages.error(request, 'Acesso negado. Apenas administradores podem criar clientes.')
        return redirect('home')

    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente cadastrado com sucesso!')
            return redirect('list_cliente')
        else:
            messages.error(request, 'Erro ao cadastrar cliente.')
    else:
        form = ClienteForm()

    context = {'form': form}
    return render(request, 'log/criar_cliente.html', context)


@login_required
@user_passes_test(can_edit_clientes, login_url='/login/')
def atualizar_cliente(request, id):
    """Atualizar cliente existente - Apenas admin"""
    if not request.user.is_staff:
        messages.error(request, 'Acesso negado. Apenas administradores podem editar clientes.')
        return redirect('home')

    cliente = get_object_or_404(Cliente, id=id)

    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            messages.success(request, 'Dados do cliente atualizados com sucesso!')
            return redirect('list_cliente')
        else:
            messages.error(request, 'Erro ao atualizar cliente.')
    else:
        form = ClienteForm(instance=cliente)

    context = {
        'form': form,
        'cliente': cliente,
    }
    return render(request, 'log/atualizar_cliente.html', context)


@login_required
@user_passes_test(can_edit_clientes, login_url='/login/')
def deletar_cliente(request, id):
    """Deletar cliente - Apenas admin"""
    if not request.user.is_staff:
        messages.error(request, 'Acesso negado. Apenas administradores podem deletar clientes.')
        return redirect('home')

    cliente = get_object_or_404(Cliente, id=id)
    nome = cliente.nome
    cliente.delete()
    messages.success(request, f'Cliente "{nome}" deletado com sucesso!')
    return redirect('list_cliente')


# CRUD VEÍCULO -------------------------------------

@login_required
@user_passes_test(can_view_veiculos, login_url='/login/')
def list_veiculo(request):
    """Lista todos os veículos - Admin ou motorista"""
    if request.user.is_staff:
        veiculos = Veiculo.objects.all().select_related('motorista').order_by('placa')
    elif hasattr(request.user, 'motorista'):
        # Motorista vê apenas veículos associados a ele
        veiculos = Veiculo.objects.filter(motorista=request.user.motorista).select_related('motorista').order_by(
            'placa')
    else:
        veiculos = Veiculo.objects.none()

    context = {
        'veiculos': veiculos,
        'total': veiculos.count(),
    }
    return render(request, 'log/list_veiculo.html', context)


@login_required
@user_passes_test(can_edit_veiculos, login_url='/login/')
def criar_veiculo(request):
    """Criar novo veículo - Apenas admin"""
    if not request.user.is_staff:
        messages.error(request, 'Acesso negado. Apenas administradores podem criar veículos.')
        return redirect('home')

    if request.method == 'POST':
        form = VeiculoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Veículo cadastrado com sucesso!')
            return redirect('list_veiculo')
        else:
            messages.error(request, 'Erro ao cadastrar veículo.')
    else:
        form = VeiculoForm()

    context = {'form': form}
    return render(request, 'log/criar_veiculo.html', context)


@login_required
@user_passes_test(can_edit_veiculos, login_url='/login/')
def atualizar_veiculo(request, id):
    """Atualizar veículo existente - Apenas admin"""
    if not request.user.is_staff:
        messages.error(request, 'Acesso negado. Apenas administradores podem editar veículos.')
        return redirect('home')

    veiculo = get_object_or_404(Veiculo, id=id)

    if request.method == 'POST':
        form = VeiculoForm(request.POST, instance=veiculo)
        if form.is_valid():
            form.save()
            messages.success(request, 'Dados do veículo atualizados com sucesso!')
            return redirect('list_veiculo')
        else:
            messages.error(request, 'Erro ao atualizar veículo.')
    else:
        form = VeiculoForm(instance=veiculo)

    context = {
        'form': form,
        'veiculo': veiculo,
    }
    return render(request, 'log/atualizar_veiculo.html', context)


@login_required
@user_passes_test(can_edit_veiculos, login_url='/login/')
def deletar_veiculo(request, id):
    """Deletar veículo - Apenas admin"""
    if not request.user.is_staff:
        messages.error(request, 'Acesso negado. Apenas administradores podem deletar veículos.')
        return redirect('home')

    veiculo = get_object_or_404(Veiculo, id=id)
    placa = veiculo.placa
    veiculo.delete()
    messages.success(request, f'Veículo "{placa}" deletado com sucesso!')
    return redirect('list_veiculo')


# CRUD ENTREGA -------------------------------------

@login_required
@user_passes_test(can_view_entregas, login_url='/login/')
def list_entrega(request):
    """Lista todas as entregas - Admin ou motorista"""
    if request.user.is_staff:
        entregas = Entrega.objects.all().select_related('cliente', 'motorista', 'rota').order_by('-data_solicitacao')
    elif hasattr(request.user, 'motorista'):
        # Motorista vê apenas suas entregas
        entregas = Entrega.objects.filter(motorista=request.user.motorista).select_related('cliente', 'motorista',
                                                                                           'rota').order_by(
            '-data_solicitacao')
    else:
        entregas = Entrega.objects.none()

    context = {
        'entregas': entregas,
        'total': entregas.count(),
        'sem_rota': entregas.filter(rota__isnull=True).count(),
    }
    return render(request, 'log/list_entrega.html', context)


@login_required
@user_passes_test(can_edit_entregas, login_url='/login/')
def criar_entrega(request):
    """Criar nova entrega - Admin ou motorista"""
    if request.method == 'POST':
        form = EntregaForm(request.POST)
        if form.is_valid():
            entrega = form.save(commit=False)
            # Se for motorista, atribuir automaticamente a ele
            if hasattr(request.user, 'motorista') and not entrega.motorista:
                entrega.motorista = request.user.motorista
            entrega.save()
            messages.success(request, f'Entrega "{entrega.codigo_rastreio}" registrada com sucesso!')
            return redirect('list_entrega')
        else:
            messages.error(request, 'Erro ao registrar entrega. Verifique os dados.')
    else:
        form = EntregaForm()

    context = {'form': form}
    return render(request, 'log/criar_entrega.html', context)


@login_required
def atualizar_entrega(request, id):
    """Atualizar entrega existente - Admin ou motorista (apenas suas)"""
    entrega = get_object_or_404(Entrega, id=id)

    # Verificar permissão
    if not can_edit_entrega(request.user, entrega):
        messages.error(request, 'Acesso negado. Você só pode editar suas próprias entregas.')
        return redirect('list_entrega')

    if request.method == 'POST':
        form = EntregaForm(request.POST, instance=entrega)
        if form.is_valid():
            # Se for motorista, garantir que a entrega continue sendo dele
            if hasattr(request.user, 'motorista') and not request.user.is_staff:
                form.instance.motorista = request.user.motorista

            # Verificar mudança de rota
            nova_rota = form.cleaned_data.get('rota')
            if nova_rota and entrega.rota != nova_rota:
                if not entrega.pode_ser_adicionada_na_rota(nova_rota):
                    messages.warning(request, 'Capacidade da rota excedida! Rota não foi alterada.')
                    form.instance.rota = entrega.rota  # Manter rota anterior

            form.save()
            messages.success(request, 'Dados da entrega atualizados com sucesso!')
            return redirect('list_entrega')
        else:
            messages.error(request, 'Erro ao atualizar entrega.')
    else:
        form = EntregaForm(instance=entrega)

    context = {
        'form': form,
        'entrega': entrega,
    }
    return render(request, 'log/atualizar_entrega.html', context)


@login_required
def deletar_entrega(request, id):
    """Deletar entrega - Admin ou motorista (apenas suas)"""
    entrega = get_object_or_404(Entrega, id=id)

    # Verificar permissão
    if not can_edit_entrega(request.user, entrega):
        messages.error(request, 'Acesso negado. Você só pode deletar suas próprias entregas.')
        return redirect('list_entrega')

    codigo = entrega.codigo_rastreio
    entrega.delete()
    messages.success(request, f'Entrega "{codigo}" deletada com sucesso!')
    return redirect('list_entrega')


# CRUD ROTA -------------------------------------

@login_required
@user_passes_test(can_view_rotas, login_url='/login/')
def list_rota(request):
    """Lista todas as rotas - Admin ou motorista"""
    if request.user.is_staff:
        rotas = Rota.objects.all().select_related('motorista', 'veiculo').prefetch_related('entregas').order_by(
            '-data_rota')
    elif hasattr(request.user, 'motorista'):
        # Motorista vê apenas suas rotas
        rotas = Rota.objects.filter(motorista=request.user.motorista).select_related('motorista',
                                                                                     'veiculo').prefetch_related(
            'entregas').order_by('-data_rota')
    else:
        rotas = Rota.objects.none()

    context = {
        'rotas': rotas,
        'total': rotas.count(),
    }
    return render(request, 'log/list_rota.html', context)


@login_required
def lista_entregas(request, rota_id):
    """Lista entregas de uma rota específica - Admin ou motorista (apenas suas)"""
    rota = get_object_or_404(Rota, id=rota_id)

    # Verificar permissão
    if not can_view_rota(request.user, rota):
        messages.error(request, 'Acesso negado. Você só pode ver suas próprias rotas.')
        return redirect('list_rota')

    entregas = rota.entregas.all().select_related('cliente', 'motorista')

    # Filtrar entregas disponíveis conforme permissão
    if request.user.is_staff:
        entregas_disponiveis = Entrega.objects.filter(rota__isnull=True, status='pendente').select_related('cliente')
    elif hasattr(request.user, 'motorista'):
        entregas_disponiveis = Entrega.objects.filter(
            rota__isnull=True,
            status='pendente',
            motorista=request.user.motorista
        ).select_related('cliente')
    else:
        entregas_disponiveis = Entrega.objects.none()

    context = {
        'rota': rota,
        'entregas': entregas,
        'entregas_disponiveis': entregas_disponiveis,
        'capacidade_utilizada': rota.capacidade_total_utilizada(),
        'capacidade_disponivel': rota.veiculo.capacidade_maxima - rota.capacidade_total_utilizada(),
        'total_entregas': rota.total_entregas(),
        'valor_total': rota.valor_total_entregas(),
    }
    return render(request, 'log/lista_entregas.html', context)


@login_required
@user_passes_test(can_edit_rotas, login_url='/login/')
def criar_rota(request):
    """Criar nova rota - Apenas admin"""
    if not request.user.is_staff:
        messages.error(request, 'Acesso negado. Apenas administradores podem criar rotas.')
        return redirect('home')

    if request.method == 'POST':
        form = RotaForm(request.POST)
        if form.is_valid():
            rota = form.save()

            # Atualizar status do veículo e motorista
            veiculo = rota.veiculo
            veiculo.status = "em_uso"
            veiculo.save()

            motorista = rota.motorista
            motorista.status = "em_rota"
            motorista.save()

            messages.success(request, f'Rota "{rota.nome}" registrada com sucesso!')
            return redirect('list_rota')
        else:
            messages.error(request, 'Erro ao registrar rota.')
    else:
        form = RotaForm()

    context = {'form': form}
    return render(request, 'log/criar_rota.html', context)


@login_required
@user_passes_test(can_edit_rotas, login_url='/login/')
def atualizar_rota(request, id):
    """Atualizar rota existente - Apenas admin"""
    if not request.user.is_staff:
        messages.error(request, 'Acesso negado. Apenas administradores podem editar rotas.')
        return redirect('home')

    rota = get_object_or_404(Rota, id=id)

    if request.method == 'POST':
        form = RotaForm(request.POST, instance=rota)
        if form.is_valid():
            rota = form.save()

            # Se rota foi concluída, liberar veículo e motorista
            if rota.status == "concluida":
                rota.veiculo.status = "disponivel"
                rota.veiculo.save()
                rota.motorista.status = "disponivel"
                rota.motorista.save()
                messages.success(request, f'Rota "{rota.nome}" concluída! Veículo e motorista liberados.')
            else:
                messages.success(request, 'Dados da rota atualizados com sucesso!')

            return redirect('list_rota')
        else:
            messages.error(request, 'Erro ao atualizar rota.')
    else:
        form = RotaForm(instance=rota)

    context = {
        'form': form,
        'rota': rota,
    }
    return render(request, 'log/atualizar_rota.html', context)


@login_required
@user_passes_test(can_edit_rotas, login_url='/login/')
def deletar_rota(request, id):
    """Deletar rota - Apenas admin"""
    if not request.user.is_staff:
        messages.error(request, 'Acesso negado. Apenas administradores podem deletar rotas.')
        return redirect('home')

    rota = get_object_or_404(Rota, id=id)

    # Remover entregas da rota antes de deletar
    entregas = rota.entregas.all()
    for entrega in entregas:
        entrega.rota = None
        entrega.save()

    # Liberar veículo e motorista
    if rota.veiculo:
        rota.veiculo.status = "disponivel"
        rota.veiculo.save()

    if rota.motorista:
        rota.motorista.status = "disponivel"
        rota.motorista.save()

    nome = rota.nome
    rota.delete()
    messages.success(request, f'Rota "{nome}" deletada com sucesso! Entregas foram liberadas.')
    return redirect('list_rota')


@login_required
def adicionar_entrega_rota(request, rota_id):
    """Adicionar entrega a uma rota - Admin ou motorista (apenas suas rotas)"""
    rota = get_object_or_404(Rota, id=rota_id)

    # Verificar permissão
    if not can_edit_rotas(request.user):
        messages.error(request, 'Acesso negado. Apenas administradores podem gerenciar rotas.')
        return redirect('list_rota')

    if request.method == 'POST':
        entrega_id = request.POST.get('entrega_id')

        try:
            entrega = Entrega.objects.get(id=entrega_id)

            # Validações
            if entrega.rota is not None:
                messages.error(request, f'A entrega "{entrega.codigo_rastreio}" já está em outra rota!')
            elif not entrega.pode_ser_adicionada_na_rota(rota):
                messages.error(request,
                               f'Capacidade excedida! A entrega "{entrega.codigo_rastreio}" precisa de {entrega.capacidade_necessaria}kg, mas só há {rota.veiculo.capacidade_maxima - rota.capacidade_total_utilizada()}kg disponíveis.')
            else:
                entrega.rota = rota
                entrega.save()
                messages.success(request, f'Entrega "{entrega.codigo_rastreio}" adicionada à rota com sucesso!')

        except Entrega.DoesNotExist:
            messages.error(request, 'Entrega não encontrada!')

    return redirect('lista_entregas', rota_id=rota_id)


@login_required
def remover_entrega_rota(request, entrega_id):
    """Remover entrega de uma rota - Admin ou motorista (apenas suas entregas)"""
    entrega = get_object_or_404(Entrega, id=entrega_id)

    # Verificar permissão para editar a entrega
    if not can_edit_entrega(request.user, entrega):
        messages.error(request, 'Acesso negado. Você só pode gerenciar suas próprias entregas.')
        return redirect('list_entrega')

    rota_id = entrega.rota.id if entrega.rota else None

    if entrega.rota:
        # Verificar permissão para editar a rota (se houver)
        if entrega.rota and not can_edit_rotas(request.user):
            messages.error(request, 'Acesso negado. Apenas administradores podem gerenciar rotas.')
            return redirect('list_entrega')

        codigo = entrega.codigo_rastreio
        entrega.rota = None
        entrega.save()
        messages.success(request, f'Entrega "{codigo}" removida da rota com sucesso!')
    else:
        messages.warning(request, 'Esta entrega não está em nenhuma rota.')

    if rota_id:
        return redirect('lista_entregas', rota_id=rota_id)
    else:
        return redirect('list_entrega')


# FUNÇÕES AUXILIARES -------------------------------------

def calcula_capacidade_total(rota):
    """Calcula capacidade total utilizada na rota"""
    return sum([e.capacidade_necessaria for e in rota.entregas.all()])