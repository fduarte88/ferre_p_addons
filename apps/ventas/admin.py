from django.contrib import admin
from .models import Cliente, Venta, DetalleVenta


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'identificacion', 'tipo', 'telefono', 'activo')
    list_filter = ('tipo', 'activo')
    search_fields = ('nombre', 'identificacion')


class DetalleVentaInline(admin.TabularInline):
    model = DetalleVenta
    extra = 0


@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    list_display = ('pk', 'cliente', 'vendedor', 'fecha', 'total', 'estado')
    list_filter = ('estado', 'metodo_pago')
    search_fields = ('cliente__nombre',)
    inlines = [DetalleVentaInline]
