from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Venta, Cliente, DetalleVenta
from .forms import VentaForm, ClienteForm, DetalleVentaForm
from apps.productos.models import Producto
import json


@login_required
def lista_ventas(request):
    query = request.GET.get('q', '')
    ventas = Venta.objects.select_related('cliente', 'vendedor').all()
    if query:
        ventas = ventas.filter(
            Q(cliente__nombre__icontains=query) | Q(pk__icontains=query)
        )
    return render(request, 'ventas/lista.html', {
        'ventas': ventas,
        'query': query,
        'titulo': 'Ventas',
    })


@login_required
def nueva_venta(request):
    productos = Producto.objects.filter(activo=True, stock__gt=0).values(
        'id', 'nombre', 'codigo', 'precio_venta', 'stock'
    )
    clientes = Cliente.objects.filter(activo=True)
    if request.method == 'POST':
        form = VentaForm(request.POST)
        items = json.loads(request.POST.get('items', '[]'))
        if form.is_valid() and items:
            venta = form.save(commit=False)
            venta.vendedor = request.user
            venta.save()
            for item in items:
                producto = Producto.objects.get(pk=item['producto_id'])
                DetalleVenta.objects.create(
                    venta=venta,
                    producto=producto,
                    cantidad=item['cantidad'],
                    precio_unitario=item['precio'],
                    descuento=item.get('descuento', 0),
                )
                producto.stock -= item['cantidad']
                producto.save()
            venta.calcular_totales()
            messages.success(request, f'Venta #{venta.pk} registrada exitosamente.')
            return redirect('ventas:detalle', pk=venta.pk)
        else:
            messages.error(request, 'Agregue al menos un producto a la venta.')
    else:
        form = VentaForm()
    return render(request, 'ventas/nueva_venta.html', {
        'form': form,
        'productos': list(productos),
        'clientes': clientes,
        'titulo': 'Nueva Venta',
    })


@login_required
def detalle_venta(request, pk):
    venta = get_object_or_404(Venta.objects.select_related('cliente', 'vendedor'), pk=pk)
    detalles = venta.detalles.select_related('producto').all()
    return render(request, 'ventas/detalle.html', {
        'venta': venta,
        'detalles': detalles,
        'titulo': f'Venta #{venta.pk}',
    })


@login_required
def anular_venta(request, pk):
    venta = get_object_or_404(Venta, pk=pk)
    if request.method == 'POST' and venta.estado != 'anulada':
        for detalle in venta.detalles.all():
            detalle.producto.stock += detalle.cantidad
            detalle.producto.save()
        venta.estado = 'anulada'
        venta.save()
        messages.success(request, f'Venta #{venta.pk} anulada.')
    return redirect('ventas:lista')


@login_required
def lista_clientes(request):
    query = request.GET.get('q', '')
    clientes = Cliente.objects.filter(activo=True)
    if query:
        clientes = clientes.filter(
            Q(nombre__icontains=query) | Q(identificacion__icontains=query)
        )
    return render(request, 'ventas/clientes.html', {
        'clientes': clientes,
        'query': query,
        'titulo': 'Clientes',
    })


@login_required
def crear_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente creado exitosamente.')
            return redirect('ventas:clientes')
    else:
        form = ClienteForm()
    return render(request, 'ventas/cliente_form.html', {'form': form, 'titulo': 'Nuevo Cliente'})


@login_required
def editar_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente actualizado.')
            return redirect('ventas:clientes')
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'ventas/cliente_form.html', {'form': form, 'titulo': 'Editar Cliente'})
