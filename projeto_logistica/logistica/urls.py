from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import custom_logout


urlpatterns = [
    path('', views.home, name='home'),
    path(
        'login/',
        auth_views.LoginView.as_view(
            template_name='log/login.html',
            redirect_authenticated_user=True
        ),
        name='login'
        ),
    path('logout/', custom_logout, name='logout'),

    path('list_motorista/', views.list_motorista, name='list_motorista'),
    path('criar_motorista/', views.criar_motorista, name='criar_motorista'),
    path('deletar_motorista/<int:id>', views.deletar_motorista, name='deletar_motorista'),
    path('atualizar_motorista/<int:id>', views.atualizar_motorista, name='atualizar_motorista'),
]