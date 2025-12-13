from django.shortcuts import redirect
from django.urls import reverse


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