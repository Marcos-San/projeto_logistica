from .permissions import get_motorista_from_user, is_motorista


def user_permissions(request):
    """Adiciona informações de permissão do usuário ao contexto de todos os templates"""
    context = {}

    if request.user.is_authenticated:
        # 1. Informações básicas
        context['is_admin'] = request.user.is_staff

        # 2. Verificar se é motorista usando a função do permissions.py
        context['is_motorista'] = is_motorista(request.user)

        # 3. Obter o objeto motorista se existir
        motorista = get_motorista_from_user(request.user)
        if motorista:
            context['user_motorista'] = motorista
            context['motorista_nome'] = motorista.nome
            context['motorista_id'] = motorista.id

        # 4. Tipo de perfil para lógica no template
        if request.user.is_staff:
            context['user_profile'] = 'admin'
        elif motorista:
            context['user_profile'] = 'motorista'
        else:
            context['user_profile'] = 'cliente'

    return context