from django.urls import path
from django.contrib.auth import views as auth_views
from . import views_html as views

urlpatterns = [
    path('', views.home, name='home'),

    path(
        'login/',
        auth_views.LoginView.as_view(
            template_name='log/login.html',
            redirect_authenticated_user=True,
            next_page='redirecionar_perfil'
        ),
        name='login'
    ),

    path('logout/', views.custom_logout, name='logout'),
    path('redirecionar-perfil/', views.redirecionar_por_perfil, name='redirecionar_perfil'),
    path('buscar_entrega/', views.buscar_entrega, name='buscar_entrega'),

    path('motoristas/', views.list_motorista, name='list_motorista'),
    path('motoristas/criar/', views.criar_motorista, name='criar_motorista'),
    path('motoristas/<int:id>/', views.detalhes_motorista, name='detalhes_motorista'),
    path('motoristas/<int:id>/editar/', views.atualizar_motorista, name='atualizar_motorista'),
    path('motoristas/<int:id>/deletar/', views.deletar_motorista, name='deletar_motorista'),

    path(
        'motoristas/<int:id>/acesso/',
        views.gerenciar_acesso_motorista,
        name='gerenciar_acesso_motorista'
    ),

    path(
        'motoristas/<int:id>/acesso/criar-usuario/',
        views.criar_usuario_motorista,
        name='criar_usuario_motorista'
    ),

    path(
        'motoristas/verificar-grupos/',
        views.verificar_grupos_motoristas,
        name='verificar_grupos_motoristas'
    ),

    path(
        'motoristas/verificar-todos-grupos/',
        views.verificar_todos_grupos,
        name='verificar_todos_grupos'
    ),


    path('clientes/', views.list_cliente, name='list_cliente'),
    path('clientes/criar/', views.criar_cliente, name='criar_cliente'),
    path('clientes/<int:id>/editar/', views.atualizar_cliente, name='atualizar_cliente'),
    path('clientes/<int:id>/deletar/', views.deletar_cliente, name='deletar_cliente'),

    path('veiculos/', views.list_veiculo, name='list_veiculo'),
    path('veiculos/criar/', views.criar_veiculo, name='criar_veiculo'),
    path('veiculos/<int:id>/editar/', views.atualizar_veiculo, name='atualizar_veiculo'),
    path('veiculos/<int:id>/deletar/', views.deletar_veiculo, name='deletar_veiculo'),

    path('entregas/', views.list_entrega, name='list_entrega'),
    path('entregas/criar/', views.criar_entrega, name='criar_entrega'),
    path('entregas/<int:id>/editar/', views.atualizar_entrega, name='atualizar_entrega'),
    path('entregas/<int:id>/deletar/', views.deletar_entrega, name='deletar_entrega'),

    path('rotas/', views.list_rota, name='list_rota'),
    path('rotas/criar/', views.criar_rota, name='criar_rota'),
    path('rotas/<int:id>/editar/', views.atualizar_rota, name='atualizar_rota'),
    path('rotas/<int:id>/deletar/', views.deletar_rota, name='deletar_rota'),

    path(
        'rotas/<int:rota_id>/entregas/',
        views.lista_entregas,
        name='lista_entregas'
    ),

    path(
        'rotas/<int:rota_id>/adicionar-entrega/',
        views.adicionar_entrega_rota,
        name='adicionar_entrega_rota'
    ),

    path(
        'entregas/<int:entrega_id>/remover-rota/',
        views.remover_entrega_rota,
        name='remover_entrega_rota'
    ),
]