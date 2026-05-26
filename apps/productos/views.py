from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Producto, Categoria
from .forms import ProductoForm, CategoriaForm


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
        form = ProductoForm()
    return render(request, 'productos/form.html', {'form': form, 'titulo': 'Nuevo Producto'})


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
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoría creada exitosamente.')
            return redirect('productos:categorias')
    else:
        form = CategoriaForm()
    return render(request, 'productos/categoria_form.html', {'form': form, 'titulo': 'Nueva Categoría'})


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
