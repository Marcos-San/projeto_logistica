from django.contrib.auth.decorators import user_passes_test
from rest_framework.permissions import BasePermission, SAFE_METHODS
from .models import Motorista


def is_admin(user):
    """Verifica se o usuário é administrador"""
    return user.is_authenticated and user.is_staff


def is_motorista(user):
    """Verifica se o usuário tem perfil de motorista"""
    if not user.is_authenticated:
        return False

    # Verificar de múltiplas formas
    if hasattr(user, 'motorista_profile') and user.motorista_profile is not None:
        return True

    try:
        Motorista.objects.get(user=user)
        return True
    except Motorista.DoesNotExist:
        pass

    if hasattr(user, 'perfil') and user.perfil.motorista is not None:
        return True

    return False


def is_admin_or_motorista(user):
    """Verifica se o usuário é admin ou motorista"""
    if not user.is_authenticated:
        return False

    return is_admin(user) or is_motorista(user)


def can_view_entregas(user):
    """Verifica se o usuário pode visualizar entregas"""
    return is_admin_or_motorista(user)  # CORRIGIDO: usa a função unificada


def can_edit_entregas(user):
    """Verifica se o usuário pode editar entregas"""
    return is_admin_or_motorista(user)  # CORRIGIDO: usa a função unificada


def can_view_motoristas(user):
    """Verifica se o usuário pode visualizar motoristas"""
    return is_admin(user)  # CORRIGIDO: apenas admin pode ver lista de motoristas


def can_edit_motoristas(user):
    """Verifica se o usuário pode editar motoristas"""
    return is_admin(user)  # CORRIGIDO: apenas admin pode editar motoristas


def can_view_veiculos(user):
    """Verifica se o usuário pode visualizar veículos"""
    return is_admin_or_motorista(user)  # CORRIGIDO: usa a função unificada


def can_edit_veiculos(user):
    """Verifica se o usuário pode editar veículos"""
    return is_admin(user)  # CORRIGIDO: apenas admin pode editar veículos


def can_view_clientes(user):
    """Verifica se o usuário pode visualizar clientes"""
    return is_admin_or_motorista(user)  # CORRIGIDO: usa a função unificada


def can_edit_clientes(user):
    """Verifica se o usuário pode editar clientes"""
    return is_admin(user)  # CORRIGIDO: apenas admin pode editar clientes


def can_view_rotas(user):
    """Verifica se o usuário pode visualizar rotas"""
    return is_admin_or_motorista(user)  # CORRIGIDO: usa a função unificada


def can_edit_rotas(user):
    """Verifica se o usuário pode editar rotas"""
    return is_admin(user)  # CORRIGIDO: apenas admin pode editar rotas


# Decorators personalizados
def admin_required(view_func):
    """Decorator que requer que o usuário seja admin"""
    actual_decorator = user_passes_test(
        lambda u: is_admin(u),
        login_url='/login/',
        redirect_field_name=None
    )
    return actual_decorator(view_func)


def motorista_required(view_func):
    """Decorator que requer que o usuário seja motorista"""
    actual_decorator = user_passes_test(
        lambda u: is_motorista(u),
        login_url='/login/',
        redirect_field_name=None
    )
    return actual_decorator(view_func)


def admin_or_motorista_required(view_func):
    """Decorator que requer que o usuário seja admin ou motorista"""
    actual_decorator = user_passes_test(
        lambda u: is_admin_or_motorista(u),
        login_url='/login/',
        redirect_field_name=None
    )
    return actual_decorator(view_func)


# Funções auxiliares para obter motorista do usuário
def get_motorista_from_user(user):
    """Obtém o objeto motorista do usuário de forma segura"""
    if not user.is_authenticated:
        return None

    # Primeiro tenta pelo related_name
    if hasattr(user, 'motorista_profile') and user.motorista_profile:
        return user.motorista_profile

    # Tenta pelo banco
    try:
        return Motorista.objects.get(user=user)
    except Motorista.DoesNotExist:
        pass

    # Tenta pelo perfil
    if hasattr(user, 'perfil') and user.perfil.motorista:
        return user.perfil.motorista

    return None


# Funções de verificação de permissão para objetos específicos
def can_view_motorista(user, motorista_obj):
    """Verifica se o usuário pode visualizar um motorista específico"""
    if not user.is_authenticated:
        return False

    if is_admin(user):  # CORRIGIDO: usa a função unificada
        return True

    # Motorista pode ver apenas seu próprio perfil
    user_motorista = get_motorista_from_user(user)  # CORRIGIDO: usa função auxiliar
    if user_motorista:
        return user_motorista.id == motorista_obj.id

    return False


def can_edit_motorista(user, motorista_obj):
    """Verifica se o usuário pode editar um motorista específico"""
    if not user.is_authenticated:
        return False

    if is_admin(user):  # CORRIGIDO: usa a função unificada
        return True

    # Motorista pode editar apenas seu próprio perfil
    user_motorista = get_motorista_from_user(user)  # CORRIGIDO: usa função auxiliar
    if user_motorista:
        return user_motorista.id == motorista_obj.id

    return False


def can_view_entrega(user, entrega_obj):
    """Verifica se o usuário pode visualizar uma entrega específica"""
    if not user.is_authenticated:
        return False

    if is_admin(user):  # CORRIGIDO: usa a função unificada
        return True

    # Motorista pode ver apenas suas próprias entregas
    user_motorista = get_motorista_from_user(user)  # CORRIGIDO: usa função auxiliar
    if user_motorista:
        return entrega_obj.motorista and entrega_obj.motorista.id == user_motorista.id

    return False


def can_edit_entrega(user, entrega_obj):
    """Verifica se o usuário pode editar uma entrega específica"""
    if not user.is_authenticated:
        return False

    if is_admin(user):  # CORRIGIDO: usa a função unificada
        return True

    # Motorista pode editar apenas suas próprias entregas
    user_motorista = get_motorista_from_user(user)  # CORRIGIDO: usa função auxiliar
    if user_motorista:
        return entrega_obj.motorista and entrega_obj.motorista.id == user_motorista.id

    return False


def can_view_rota(user, rota_obj):
    """Verifica se o usuário pode visualizar uma rota específica"""
    if not user.is_authenticated:
        return False

    if is_admin(user):  # CORRIGIDO: usa a função unificada
        return True

    # Motorista pode ver apenas suas próprias rotas
    user_motorista = get_motorista_from_user(user)  # CORRIGIDO: usa função auxiliar
    if user_motorista:
        return rota_obj.motorista and rota_obj.motorista.id == user_motorista.id

    return False


def can_view_veiculo(user, veiculo_obj):
    """Verifica se o usuário pode visualizar um veículo específico"""
    if not user.is_authenticated:
        return False

    if is_admin(user):  # CORRIGIDO: usa a função unificada
        return True

    # Motorista pode ver apenas veículo associado a ele
    user_motorista = get_motorista_from_user(user)  # CORRIGIDO: usa função auxiliar
    if user_motorista:
        return veiculo_obj.motorista and veiculo_obj.motorista.id == user_motorista.id

    return False


# Funções para uso em templates (se necessário)
def user_is_motorista(user):
    """Função simplificada para uso em templates"""
    return is_motorista(user)


def user_is_admin_or_motorista(user):
    """Função simplificada para uso em templates"""
    return is_admin_or_motorista(user)