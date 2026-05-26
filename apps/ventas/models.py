from django.db import models
from django.contrib.auth.models import User
from apps.productos.models import Producto


class Cliente(models.Model):
    TIPOS = [
        ('natural', 'Persona Natural'),
        ('juridica', 'Persona Jurídica'),
    ]
    tipo = models.CharField(max_length=10, choices=TIPOS, default='natural')
    nombre = models.CharField(max_length=200)
    identificacion = models.CharField(max_length=20, unique=True)
    telefono = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    direccion = models.TextField(blank=True)
    activo = models.BooleanField(default=True)
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['nombre']

    def __str__(self):
        return f'{self.nombre} ({self.identificacion})'


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
        self.impuesto = self.subtotal * 19 / 100
        self.total = self.subtotal + self.impuesto - self.descuento
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
