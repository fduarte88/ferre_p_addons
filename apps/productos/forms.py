from django import forms
from .models import Producto, Categoria

UNIDAD_CHOICES = [
    ('Unidad', 'Unidad'),
    ('Metro', 'Metro'),
    ('Metro cuadrado', 'Metro cuadrado'),
    ('Metro cúbico', 'Metro cúbico'),
    ('Kilogramo', 'Kilogramo'),
    ('Gramo', 'Gramo'),
    ('Litro', 'Litro'),
    ('Mililitro', 'Mililitro'),
    ('Caja', 'Caja'),
    ('Paquete', 'Paquete'),
    ('Bolsa', 'Bolsa'),
    ('Rollo', 'Rollo'),
    ('Par', 'Par'),
    ('Juego', 'Juego'),
    ('Docena', 'Docena'),
    ('Saco', 'Saco'),
    ('Galón', 'Galón'),
    ('Tubo', 'Tubo'),
    ('Plancha', 'Plancha'),
    ('Otro', 'Otro'),
]


class ProductoForm(forms.ModelForm):
    unidad = forms.ChoiceField(
        choices=UNIDAD_CHOICES,
        initial='Unidad',
        widget=forms.Select(attrs={'class': 'form-select'}),
    )

    class Meta:
        model = Producto
        fields = ['codigo', 'nombre', 'descripcion', 'categoria', 'precio_compra',
                  'precio_venta', 'stock', 'stock_minimo', 'unidad', 'imagen', 'activo']
        widgets = {
            'codigo': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'categoria': forms.Select(attrs={'class': 'form-select'}),
            'precio_compra': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'precio_venta': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
            'stock_minimo': forms.NumberInput(attrs={'class': 'form-control'}),
            'imagen': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def clean_codigo_barra(self):
        value = (self.cleaned_data.get('codigo_barra') or '').strip()
        return value if value else None


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre', 'descripcion', 'activo']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
