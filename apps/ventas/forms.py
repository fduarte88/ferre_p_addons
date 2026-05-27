from django import forms
from .models import Venta, Cliente


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['tipo', 'ruc', 'nombre', 'apellido', 'email', 'telefono', 'direccion', 'activo']
        widgets = {
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'ruc': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'XXXXXXXX-D'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }


class VentaForm(forms.ModelForm):
    class Meta:
        model = Venta
        fields = ['metodo_pago', 'descuento', 'observaciones']
        widgets = {
            'metodo_pago': forms.Select(attrs={'class': 'form-select'}),
            'descuento': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'value': '0'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }
