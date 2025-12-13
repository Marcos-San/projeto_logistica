from django.shortcuts import redirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin
from django.contrib import messages
from .models import PerfilUsuario, Motorista


class ProfileRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Redirecionar após login baseado no perfil
        if request.user.is_authenticated and request.path == reverse('home'):
            if hasattr(request.user, 'motorista') and not request.user.is_staff:
                # Motorista é redirecionado para suas entregas
                return redirect('list_entrega')

        return response


class VerificarGruposMiddleware(MiddlewareMixin):
    """Middleware para verificar e corrigir grupos de motoristas"""

    def process_request(self, request):
        # Só verifica se usuário está autenticado
        if not request.user.is_authenticated:
            return None

        # Ignora URLs específicas para evitar loops
        ignored_paths = [
            '/logout/',
            '/primeiro-acesso/',
            '/verificar-meu-grupo/',
            '/admin/',
        ]

        if any(request.path.startswith(path) for path in ignored_paths):
            return None

        # Verificar se é motorista
        if hasattr(request.user, 'motorista_profile'):
            # Verificar se tem grupos
            if not request.user.groups.exists():
                # Corrigir automaticamente
                from django.contrib.auth.models import Group
                grupo_motorista, _ = Group.objects.get_or_create(name='Motoristas')
                request.user.groups.add(grupo_motorista)
                request.user.save()

                messages.info(
                    request,
                    'Seu usuário foi automaticamente configurado. '
                    'Por favor, faça logout e login novamente.'
                )

                # Se for primeira vez, redirecionar para primeiro acesso
                if not request.user.last_login:
                    return redirect('primeiro_acesso_motorista')

            # Verificar especificamente grupo Motoristas
            elif not request.user.groups.filter(name='Motoristas').exists():
                # Adicionar ao grupo
                from django.contrib.auth.models import Group
                grupo_motorista = Group.objects.get(name='Motoristas')
                request.user.groups.add(grupo_motorista)
                request.user.save()

                messages.info(
                    request,
                    'Seu usuário foi adicionado ao grupo Motoristas.'
                )

        return None


class CriarPerfilMotoristaMiddleware(MiddlewareMixin):
    """Middleware para criar perfil automaticamente para motoristas"""

    def process_request(self, request):
        if not request.user.is_authenticated:
            return None

        # Ignorar URLs específicas
        ignored_paths = [
            '/logout/',
            '/admin/',
            '/primeiro-acesso/',
        ]

        if any(request.path.startswith(path) for path in ignored_paths):
            return None

        # Verificar se usuário tem perfil
        if not hasattr(request.user, 'perfil'):
            # Criar perfil se não existir
            PerfilUsuario.objects.create(user=request.user)

        # Se é motorista, garantir que tenha perfil vinculado
        perfil = getattr(request.user, 'perfil', None)
        if perfil and not perfil.motorista:
            # Verificar se há motorista vinculado a este usuário
            try:
                motorista = Motorista.objects.get(user=request.user)
                perfil.motorista = motorista
                perfil.tipo_usuario = 'motorista'
                perfil.save()
                print(f"✅ Perfil vinculado ao motorista {motorista.nome}")
            except Motorista.DoesNotExist:
                pass

        return None