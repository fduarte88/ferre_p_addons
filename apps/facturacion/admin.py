from django.contrib import admin
from .models import Factura


@admin.register(Factura)
class FacturaAdmin(admin.ModelAdmin):
    list_display = ('numero', 'venta', 'fecha', 'total', 'estado')
    list_filter = ('estado',)
    search_fields = ('numero', 'venta__cliente__nombre')
