from django.urls import path, include

urlpatterns = [
    path('', include('logistica.urls_html')),
    path('api/', include('logistica.urls_api')),
    path('api-auth/', include('rest_framework.urls')),
]
