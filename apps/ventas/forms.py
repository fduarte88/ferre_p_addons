from django import forms
from .models import Venta, DetalleVenta, Cliente


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['tipo', 'nombre', 'identificacion', 'telefono', 'email', 'direccion', 'activo']
        widgets = {
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'identificacion': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'direccion': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }


class VentaForm(forms.ModelForm):
    class Meta:
        model = Venta
        fields = ['cliente', 'metodo_pago', 'descuento', 'observaciones']
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-select'}),
            'metodo_pago': forms.Select(attrs={'class': 'form-select'}),
            'descuento': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'value': '0'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }


class DetalleVentaForm(forms.ModelForm):
    class Meta:
        model = DetalleVenta
        fields = ['producto', 'cantidad', 'precio_unitario', 'descuento']
        widgets = {
            'producto': forms.Select(attrs={'class': 'form-select'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'precio_unitario': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'descuento': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'value': '0'}),
        }
