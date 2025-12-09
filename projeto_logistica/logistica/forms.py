from django import forms

from .models import Motorista, Cliente, Veiculo, Entrega, Rota


class MotoristaForm(forms.ModelForm):
    class Meta:
        model = Motorista
        fields = "__all__"

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = "__all__"


class VeiculoForm(forms.ModelForm):
    class Meta:
        model = Veiculo
        fields = "__all__"


class EntregaForm(forms.ModelForm):
    class Meta:
        model = Entrega
        fields = "__all__"


class RotaForm(forms.ModelForm):
    class Meta:
        model = Rota
        fields = "__all__"