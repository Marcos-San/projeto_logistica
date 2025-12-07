from django import forms

from .models import Motorista, Cliente


class MotoristaForm(forms.ModelForm):
    class Meta:
        model = Motorista
        fields = "__all__"

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = "__all__"