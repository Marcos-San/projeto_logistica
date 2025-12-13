from .permissions import *


def user_permissions(request):
    """Adiciona informações de permissão do usuário ao contexto de todos os templates"""
    context = {}

    if request.user.is_authenticated:
        context['is_admin'] = request.user.is_staff
        context['is_motorista'] = hasattr(request.user, 'motorista')
        context['user_profile'] = 'admin' if request.user.is_staff else 'motorista' if hasattr(request.user,
                                                                                               'motorista') else 'user'

        # Adicionar motorista do usuário se existir
        if hasattr(request.user, 'motorista'):
            context['user_motorista'] = request.user.motorista

    return context