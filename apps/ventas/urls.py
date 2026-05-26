from django.urls import path
from . import views

app_name = 'ventas'

urlpatterns = [
    path('', views.lista_ventas, name='lista'),
    path('nueva/', views.nueva_venta, name='nueva'),
    path('<int:pk>/', views.detalle_venta, name='detalle'),
    path('<int:pk>/anular/', views.anular_venta, name='anular'),
    path('clientes/', views.lista_clientes, name='clientes'),
    path('clientes/nuevo/', views.crear_cliente, name='crear_cliente'),
    path('clientes/<int:pk>/editar/', views.editar_cliente, name='editar_cliente'),
]
