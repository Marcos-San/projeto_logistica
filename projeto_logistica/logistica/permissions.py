from django.contrib.auth.decorators import user_passes_test
from rest_framework.permissions import BasePermission, SAFE_METHODS

def is_admin(user):
    """Verifica se o usuário é administrador"""
    return user.is_authenticated and user.is_staff

def is_motorista(user):
    """Verifica se o usuário tem perfil de motorista"""
    return user.is_authenticated and hasattr(user, 'motorista_profile')

def is_admin_or_motorista(user):
    """Verifica se o usuário é admin ou motorista"""
    return user.is_authenticated and (user.is_staff or hasattr(user, 'motorista_profile'))

def can_view_entregas(user):
    """Verifica se o usuário pode visualizar entregas"""
    if not user.is_authenticated:
        return False
    return user.is_staff or hasattr(user, 'motorista_profile')

def can_edit_entregas(user):
    """Verifica se o usuário pode editar entregas"""
    if not user.is_authenticated:
        return False
    return user.is_staff or hasattr(user, 'motorista_profile')

def can_view_motoristas(user):
    """Verifica se o usuário pode visualizar motoristas"""
    if not user.is_authenticated:
        return False
    return user.is_staff  # Apenas admin pode ver lista de motoristas

def can_edit_motoristas(user):
    """Verifica se o usuário pode editar motoristas"""
    if not user.is_authenticated:
        return False
    return user.is_staff  # Apenas admin pode editar motoristas

def can_view_veiculos(user):
    """Verifica se o usuário pode visualizar veículos"""
    if not user.is_authenticated:
        return False
    return user.is_staff or hasattr(user, 'motorista_profile')

def can_edit_veiculos(user):
    """Verifica se o usuário pode editar veículos"""
    if not user.is_authenticated:
        return False
    return user.is_staff  # Apenas admin pode editar veículos

def can_view_clientes(user):
    """Verifica se o usuário pode visualizar clientes"""
    if not user.is_authenticated:
        return False
    return user.is_staff or hasattr(user, 'motorista_profile')

def can_edit_clientes(user):
    """Verifica se o usuário pode editar clientes"""
    if not user.is_authenticated:
        return False
    return user.is_staff  # Apenas admin pode editar clientes

def can_view_rotas(user):
    """Verifica se o usuário pode visualizar rotas"""
    if not user.is_authenticated:
        return False
    return user.is_staff or hasattr(user, 'motorista_profile')

def can_edit_rotas(user):
    """Verifica se o usuário pode editar rotas"""
    if not user.is_authenticated:
        return False
    return user.is_staff  # Apenas admin pode editar rotas

# Funções auxiliares para verificar permissões
def is_admin(user):
    """Verifica se o usuário é administrador"""
    return user.is_authenticated and user.is_staff

def is_motorista(user):
    """Verifica se o usuário tem perfil de motorista"""
    return user.is_authenticated and hasattr(user, 'motorista')

def is_admin_or_motorista(user):
    """Verifica se o usuário é admin ou motorista"""
    return user.is_authenticated and (user.is_staff or hasattr(user, 'motorista'))

def can_view_entregas(user):
    """Verifica se o usuário pode visualizar entregas"""
    if not user.is_authenticated:
        return False
    return user.is_staff or hasattr(user, 'motorista')

def can_edit_entregas(user):
    """Verifica se o usuário pode editar entregas"""
    if not user.is_authenticated:
        return False
    return user.is_staff or hasattr(user, 'motorista')

def can_view_motoristas(user):
    """Verifica se o usuário pode visualizar motoristas"""
    if not user.is_authenticated:
        return False
    return user.is_staff  # Apenas admin pode ver lista de motoristas

def can_edit_motoristas(user):
    """Verifica se o usuário pode editar motoristas"""
    if not user.is_authenticated:
        return False
    return user.is_staff  # Apenas admin pode editar motoristas

def can_view_veiculos(user):
    """Verifica se o usuário pode visualizar veículos"""
    if not user.is_authenticated:
        return False
    return user.is_staff or hasattr(user, 'motorista')

def can_edit_veiculos(user):
    """Verifica se o usuário pode editar veículos"""
    if not user.is_authenticated:
        return False
    return user.is_staff  # Apenas admin pode editar veículos

def can_view_clientes(user):
    """Verifica se o usuário pode visualizar clientes"""
    if not user.is_authenticated:
        return False
    return user.is_staff or hasattr(user, 'motorista')

def can_edit_clientes(user):
    """Verifica se o usuário pode editar clientes"""
    if not user.is_authenticated:
        return False
    return user.is_staff  # Apenas admin pode editar clientes

def can_view_rotas(user):
    """Verifica se o usuário pode visualizar rotas"""
    if not user.is_authenticated:
        return False
    return user.is_staff or hasattr(user, 'motorista')

def can_edit_rotas(user):
    """Verifica se o usuário pode editar rotas"""
    if not user.is_authenticated:
        return False
    return user.is_staff  # Apenas admin pode editar rotas

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

# Funções de verificação de permissão para objetos específicos
def can_view_motorista(user, motorista_obj):
    """Verifica se o usuário pode visualizar um motorista específico"""
    if not user.is_authenticated:
        return False
    if user.is_staff:
        return True
    # Motorista pode ver apenas seu próprio perfil
    if hasattr(user, 'motorista'):
        return user.motorista.id == motorista_obj.id
    return False

def can_edit_motorista(user, motorista_obj):
    """Verifica se o usuário pode editar um motorista específico"""
    if not user.is_authenticated:
        return False
    if user.is_staff:
        return True
    # Motorista pode editar apenas seu próprio perfil
    if hasattr(user, 'motorista'):
        return user.motorista.id == motorista_obj.id
    return False

def can_view_entrega(user, entrega_obj):
    """Verifica se o usuário pode visualizar uma entrega específica"""
    if not user.is_authenticated:
        return False
    if user.is_staff:
        return True
    # Motorista pode ver apenas suas próprias entregas
    if hasattr(user, 'motorista'):
        return entrega_obj.motorista and entrega_obj.motorista.id == user.motorista.id
    return False

def can_edit_entrega(user, entrega_obj):
    """Verifica se o usuário pode editar uma entrega específica"""
    if not user.is_authenticated:
        return False
    if user.is_staff:
        return True
    # Motorista pode editar apenas suas próprias entregas
    if hasattr(user, 'motorista'):
        return entrega_obj.motorista and entrega_obj.motorista.id == user.motorista.id
    return False

def can_view_rota(user, rota_obj):
    """Verifica se o usuário pode visualizar uma rota específica"""
    if not user.is_authenticated:
        return False
    if user.is_staff:
        return True
    # Motorista pode ver apenas suas próprias rotas
    if hasattr(user, 'motorista'):
        return rota_obj.motorista and rota_obj.motorista.id == user.motorista.id
    return False

def can_view_veiculo(user, veiculo_obj):
    """Verifica se o usuário pode visualizar um veículo específico"""
    if not user.is_authenticated:
        return False
    if user.is_staff:
        return True
    # Motorista pode ver apenas veículo associado a ele
    if hasattr(user, 'motorista'):
        return veiculo_obj.motorista and veiculo_obj.motorista.id == user.motorista.id
    return False