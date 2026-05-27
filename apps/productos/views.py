from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST
from .models import Producto, Categoria
from .forms import ProductoForm, CategoriaForm


def _get_next_codigo():
    """Returns next auto-numeric product code starting at 100."""
    codigos = Producto.objects.values_list('codigo', flat=True)
    nums = []
    for c in codigos:
        try:
            nums.append(int(c))
        except (ValueError, TypeError):
            pass
    return str(max(nums) + 1) if nums else '100'


@login_required
def buscar_producto(request):
    codigo = request.GET.get('codigo', '').strip()
    if not codigo:
        return JsonResponse({'found': False})
    producto = Producto.objects.filter(
        Q(codigo=codigo) | Q(codigo_barra=codigo),
        activo=True
    ).first()
    if producto:
        return JsonResponse({
            'found': True,
            'id': producto.pk,
            'nombre': producto.nombre,
            'descripcion': producto.descripcion or producto.nombre,
            'precio': float(producto.precio_venta),
            'stock': producto.stock,
            'unidad': producto.unidad,
            'codigo': producto.codigo,
            'codigo_barra': producto.codigo_barra or '',
        })
    return JsonResponse({'found': False})


@login_required
def lista_productos(request):
    query = request.GET.get('q', '')
    categoria_id = request.GET.get('categoria', '')
    productos = Producto.objects.select_related('categoria').filter(activo=True)
    if query:
        productos = productos.filter(Q(nombre__icontains=query) | Q(codigo__icontains=query))
    if categoria_id:
        productos = productos.filter(categoria_id=categoria_id)
    categorias = Categoria.objects.filter(activo=True)
    return render(request, 'productos/lista.html', {
        'productos': productos,
        'categorias': categorias,
        'query': query,
        'categoria_id': categoria_id,
        'titulo': 'Productos',
    })


@login_required
def crear_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto creado exitosamente.')
            return redirect('productos:lista')
    else:
        form = ProductoForm(initial={'codigo': _get_next_codigo()})
    return render(request, 'productos/form.html', {'form': form, 'titulo': 'Nuevo Producto', 'es_nuevo': True})


@login_required
def editar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto actualizado exitosamente.')
            return redirect('productos:lista')
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'productos/form.html', {'form': form, 'titulo': 'Editar Producto', 'producto': producto})


@login_required
def detalle_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    return render(request, 'productos/detalle.html', {'producto': producto, 'titulo': producto.nombre})


@login_required
def eliminar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        producto.activo = False
        producto.save()
        messages.success(request, 'Producto desactivado exitosamente.')
        return redirect('productos:lista')
    return render(request, 'productos/confirmar_eliminar.html', {'producto': producto})


@login_required
def lista_categorias(request):
    categorias = Categoria.objects.all()
    return render(request, 'productos/categorias.html', {'categorias': categorias, 'titulo': 'Categorías'})


@login_required
def crear_categoria(request):
    raw_next = request.GET.get('next') or request.POST.get('next') or ''
    safe_next = raw_next if url_has_allowed_host_and_scheme(raw_next, allowed_hosts={request.get_host()}) else ''
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoría creada exitosamente.')
            return redirect(safe_next or 'productos:categorias')
    else:
        form = CategoriaForm()
    return render(request, 'productos/categoria_form.html', {
        'form': form, 'titulo': 'Nueva Categoría', 'next_url': safe_next,
    })


@login_required
def editar_categoria(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoría actualizada.')
            return redirect('productos:categorias')
    else:
        form = CategoriaForm(instance=categoria)
    return render(request, 'productos/categoria_form.html', {'form': form, 'titulo': 'Editar Categoría'})


@login_required
@require_POST
def crear_categoria_ajax(request):
    form = CategoriaForm(request.POST)
    if form.is_valid():
        categoria = form.save()
        return JsonResponse({'ok': True, 'id': categoria.pk, 'nombre': categoria.nombre})
    return JsonResponse({'ok': False, 'errors': form.errors})
