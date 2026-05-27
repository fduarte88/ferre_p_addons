from django.db import models
from django.contrib.auth.models import User
from apps.productos.models import Producto


class Cliente(models.Model):
    TIPOS = [
        ('natural', 'Persona Física'),
        ('juridica', 'Persona Jurídica'),
    ]
    tipo = models.CharField(max_length=10, choices=TIPOS, default='natural')
    ruc = models.CharField(
        max_length=20, unique=True,
        verbose_name='RUC',
        help_text='Formato Paraguay: XXXXXXXX-D',
    )
    nombre = models.CharField(max_length=100, verbose_name='Nombre')
    apellido = models.CharField(max_length=100, blank=True, verbose_name='Apellido')
    email = models.EmailField(blank=True, verbose_name='Correo electrónico')
    telefono = models.CharField(max_length=20, blank=True, verbose_name='Teléfono')
    direccion = models.TextField(blank=True, verbose_name='Dirección')
    activo = models.BooleanField(default=True)
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['apellido', 'nombre']

    @property
    def nombre_completo(self):
        return f'{self.nombre} {self.apellido}'.strip()

    def __str__(self):
        return f'{self.nombre_completo} (RUC: {self.ruc})'


class Venta(models.Model):
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('completada', 'Completada'),
        ('anulada', 'Anulada'),
    ]
    METODOS_PAGO = [
        ('efectivo', 'Efectivo'),
        ('tarjeta', 'Tarjeta'),
        ('transferencia', 'Transferencia'),
        ('credito', 'Crédito'),
    ]
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, related_name='ventas')
    vendedor = models.ForeignKey(User, on_delete=models.PROTECT, related_name='ventas')
    fecha = models.DateTimeField(auto_now_add=True)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    descuento = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    impuesto = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    metodo_pago = models.CharField(max_length=20, choices=METODOS_PAGO, default='efectivo')
    estado = models.CharField(max_length=15, choices=ESTADOS, default='completada')
    observaciones = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Venta'
        verbose_name_plural = 'Ventas'
        ordering = ['-fecha']

    def __str__(self):
        return f'Venta #{self.pk} - {self.cliente.nombre}'

    def calcular_totales(self):
        self.subtotal = sum(d.subtotal for d in self.detalles.all())
        # Precio incluye IVA 10% → IVA discriminado = subtotal × 10/110
        self.impuesto = round(self.subtotal * 10 / 110, 2)
        self.total = self.subtotal - self.descuento
        self.save()


class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
    cantidad = models.IntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=12, decimal_places=2)
    descuento = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        verbose_name = 'Detalle de Venta'
        verbose_name_plural = 'Detalles de Venta'

    def save(self, *args, **kwargs):
        self.subtotal = (self.precio_unitario * self.cantidad) - self.descuento
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.producto.nombre} x {self.cantidad}'
