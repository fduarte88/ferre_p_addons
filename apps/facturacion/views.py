from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Factura
from apps.ventas.models import Venta


@login_required
def lista_facturas(request):
    query = request.GET.get('q', '')
    estado = request.GET.get('estado', '')
    facturas = Factura.objects.select_related('venta__cliente').all()
    if query:
        facturas = facturas.filter(
            Q(numero__icontains=query) | Q(venta__cliente__nombre__icontains=query)
        )
    if estado:
        facturas = facturas.filter(estado=estado)
    return render(request, 'facturacion/lista.html', {
        'facturas': facturas,
        'query': query,
        'estado_filtro': estado,
        'estados': Factura.ESTADOS,
        'titulo': 'Facturas',
    })


@login_required
def detalle_factura(request, pk):
    factura = get_object_or_404(Factura.objects.select_related('venta__cliente'), pk=pk)
    detalles = factura.venta.detalles.select_related('producto').all() if factura.venta else []
    return render(request, 'facturacion/detalle.html', {
        'factura': factura,
        'detalles': detalles,
        'titulo': f'Factura {factura.numero}',
    })


@login_required
def generar_factura(request, venta_pk):
    venta = get_object_or_404(Venta, pk=venta_pk, estado='completada')
    if hasattr(venta, 'factura'):
        messages.warning(request, 'Esta venta ya tiene una factura generada.')
        return redirect('facturacion:detalle', pk=venta.factura.pk)
    factura = Factura.desde_venta(venta)
    messages.success(request, f'Factura {factura.numero} generada exitosamente.')
    return redirect('facturacion:detalle', pk=factura.pk)


@login_required
def cambiar_estado(request, pk):
    factura = get_object_or_404(Factura, pk=pk)
    nuevo_estado = request.POST.get('estado')
    if nuevo_estado in dict(Factura.ESTADOS):
        factura.estado = nuevo_estado
        factura.save()
        messages.success(request, f'Estado actualizado a {factura.get_estado_display()}.')
    return redirect('facturacion:detalle', pk=pk)
