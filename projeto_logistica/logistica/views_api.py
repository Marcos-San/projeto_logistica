from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Motorista, Cliente, Veiculo, Entrega, Rota
from .serializers import *
from .permissions import *


# =====================
# CRUD BÁSICO
# =====================

class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    permission_classes = [IsAuthenticated]


class MotoristaViewSet(viewsets.ModelViewSet):
    queryset = Motorista.objects.all()
    serializer_class = MotoristaSerializer
    permission_classes = [IsAuthenticated]


class VeiculoViewSet(viewsets.ModelViewSet):
    queryset = Veiculo.objects.all()
    serializer_class = VeiculoSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def disponiveis(self, request):
        qs = Veiculo.objects.filter(status='disponivel')
        return Response(VeiculoSerializer(qs, many=True).data)


class EntregaViewSet(viewsets.ModelViewSet):
    queryset = Entrega.objects.all()
    serializer_class = EntregaSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['post'])
    def atribuir_motorista(self, request, pk=None):
        entrega = self.get_object()
        entrega.motorista_id = request.data.get("motorista_id")
        entrega.save()
        return Response({"status": "motorista atribuído"})


class RotaViewSet(viewsets.ModelViewSet):
    queryset = Rota.objects.all()
    serializer_class = RotaSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['get'])
    def entregas(self, request, pk=None):
        rota = self.get_object()
        return Response(EntregaSerializer(rota.entregas.all(), many=True).data)

    @action(detail=True, methods=['get'])
    def capacidade(self, request, pk=None):
        rota = self.get_object()
        usada = rota.capacidade_total_utilizada()
        return Response({
            "utilizada": usada,
            "disponivel": rota.veiculo.capacidade_maxima - usada
        })

    @action(detail=True, methods=['get'])
    def dashboard(self, request, pk=None):
        rota = self.get_object()
        return Response({
            "rota": RotaSerializer(rota).data,
            "motorista": MotoristaSerializer(rota.motorista).data,
            "veiculo": VeiculoSerializer(rota.veiculo).data,
            "entregas": EntregaSerializer(rota.entregas.all(), many=True).data
        })