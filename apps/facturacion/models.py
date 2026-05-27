from django.db import models
from apps.ventas.models import Venta


class Factura(models.Model):
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('pagada', 'Pagada'),
        ('vencida', 'Vencida'),
        ('anulada', 'Anulada'),
    ]
    venta = models.OneToOneField(Venta, on_delete=models.PROTECT, related_name='factura', null=True, blank=True)
    numero = models.CharField(max_length=20, unique=True)
    fecha = models.DateTimeField(auto_now_add=True)
    fecha_vencimiento = models.DateField(null=True, blank=True)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    impuesto = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    descuento = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    estado = models.CharField(max_length=15, choices=ESTADOS, default='pendiente')
    observaciones = models.TextField(blank=True)
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Factura'
        verbose_name_plural = 'Facturas'
        ordering = ['-fecha']

    def __str__(self):
        return f'Factura {self.numero}'

    @classmethod
    def generar_numero(cls):
        ultima = cls.objects.order_by('-id').first()
        if ultima:
            num = int(ultima.numero.split('-')[-1]) + 1
        else:
            num = 1
        return f'FACT-{num:06d}'

    @classmethod
    def desde_venta(cls, venta):
        factura = cls(
            venta=venta,
            numero=cls.generar_numero(),
            subtotal=venta.subtotal,
            impuesto=venta.impuesto,
            descuento=venta.descuento,
            total=venta.total,
        )
        factura.save()
        return factura
