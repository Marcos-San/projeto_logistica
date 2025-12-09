from django import forms

from .models import Motorista, Cliente, Veiculo


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