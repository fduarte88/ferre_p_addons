from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from apps.productos.models import Producto
from apps.ventas.models import Venta
from apps.facturacion.models import Factura


@login_required
def index(request):
    hoy = timezone.now().date()
    inicio_mes = hoy.replace(day=1)

    total_productos = Producto.objects.filter(activo=True).count()
    productos_bajo_stock = Producto.objects.filter(stock__lte=5, activo=True).count()

    ventas_hoy = Venta.objects.filter(fecha__date=hoy).count()
    ventas_mes = Venta.objects.filter(fecha__date__gte=inicio_mes)
    total_ventas_mes = sum(v.total for v in ventas_mes)

    facturas_pendientes = Factura.objects.filter(estado='pendiente').count()
    facturas_mes = Factura.objects.filter(fecha__date__gte=inicio_mes)
    total_facturado_mes = sum(f.total for f in facturas_mes)

    ultimas_ventas = Venta.objects.select_related('cliente').order_by('-fecha')[:5]

    context = {
        'total_productos': total_productos,
        'productos_bajo_stock': productos_bajo_stock,
        'ventas_hoy': ventas_hoy,
        'total_ventas_mes': total_ventas_mes,
        'facturas_pendientes': facturas_pendientes,
        'total_facturado_mes': total_facturado_mes,
        'ultimas_ventas': ultimas_ventas,
        'titulo': 'Dashboard',
    }
    return render(request, 'dashboard/index.html', context)
