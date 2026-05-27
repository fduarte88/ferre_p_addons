from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from .models import Venta, Cliente, DetalleVenta
from .forms import VentaForm, ClienteForm
from apps.productos.models import Producto
import json


@login_required
def lista_ventas(request):
    query = request.GET.get('q', '')
    ventas = Venta.objects.select_related('cliente', 'vendedor').all()
    if query:
        ventas = ventas.filter(
            Q(cliente__nombre__icontains=query) |
            Q(cliente__apellido__icontains=query) |
            Q(cliente__ruc__icontains=query) |
            Q(pk__icontains=query)
        )
    return render(request, 'ventas/lista.html', {
        'ventas': ventas,
        'query': query,
        'titulo': 'Ventas',
    })


@login_required
def buscar_cliente(request):
    ruc = request.GET.get('ruc', '').strip()
    if not ruc:
        return JsonResponse({'found': False, 'error': 'RUC vacío'})
    try:
        cliente = Cliente.objects.get(ruc=ruc, activo=True)
        return JsonResponse({
            'found': True,
            'id': cliente.pk,
            'nombre': cliente.nombre_completo,
            'ruc': cliente.ruc,
            'email': cliente.email,
            'telefono': cliente.telefono,
        })
    except Cliente.DoesNotExist:
        return JsonResponse({'found': False})


@login_required
def nueva_venta(request):
    productos = Producto.objects.filter(activo=True, stock__gt=0).values(
        'id', 'nombre', 'codigo', 'precio_venta', 'stock'
    )
    if request.method == 'POST':
        form = VentaForm(request.POST)
        items = json.loads(request.POST.get('items', '[]'))
        cliente_id = request.POST.get('cliente_id', '').strip()

        errores = []
        if not cliente_id:
            errores.append('Debe seleccionar un cliente.')
        if not items:
            errores.append('Debe agregar al menos un producto.')

        if not errores and form.is_valid():
            cliente = get_object_or_404(Cliente, pk=cliente_id, activo=True)
            venta = form.save(commit=False)
            venta.vendedor = request.user
            venta.cliente = cliente
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
            for e in errores:
                messages.error(request, e)
    else:
        form = VentaForm()

    return render(request, 'ventas/nueva_venta.html', {
        'form': form,
        'productos': list(productos),
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
    clientes = Cliente.objects.all()
    if query:
        clientes = clientes.filter(
            Q(nombre__icontains=query) |
            Q(apellido__icontains=query) |
            Q(ruc__icontains=query) |
            Q(email__icontains=query)
        )
    return render(request, 'ventas/clientes.html', {
        'clientes': clientes,
        'query': query,
        'titulo': 'Clientes',
    })


@login_required
def detalle_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    ventas = cliente.ventas.order_by('-fecha')[:10]
    return render(request, 'ventas/cliente_detalle.html', {
        'cliente': cliente,
        'ventas': ventas,
        'titulo': cliente.nombre_completo,
    })


@login_required
def crear_cliente(request):
    next_url = request.GET.get('next', '')
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente creado exitosamente.')
            next_url = request.POST.get('next', '')
            return redirect(next_url) if next_url else redirect('ventas:clientes')
    else:
        ruc_inicial = request.GET.get('ruc', '')
        form = ClienteForm(initial={'ruc': ruc_inicial})
    return render(request, 'ventas/cliente_form.html', {
        'form': form,
        'titulo': 'Nuevo Cliente',
        'next_url': next_url,
    })


@login_required
def editar_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente actualizado.')
            return redirect('ventas:detalle_cliente', pk=pk)
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'ventas/cliente_form.html', {
        'form': form,
        'titulo': 'Editar Cliente',
        'cliente': cliente,
    })


@login_required
def eliminar_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        if cliente.ventas.exists():
            cliente.activo = False
            cliente.save()
            messages.warning(request, f'{cliente.nombre_completo} desactivado (tiene ventas asociadas).')
        else:
            cliente.delete()
            messages.success(request, 'Cliente eliminado.')
        return redirect('ventas:clientes')
    return render(request, 'ventas/cliente_confirmar_eliminar.html', {'cliente': cliente})
