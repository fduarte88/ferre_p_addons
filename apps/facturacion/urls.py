from django.urls import path
from . import views

app_name = 'facturacion'

urlpatterns = [
    path('', views.lista_facturas, name='lista'),
    path('<int:pk>/', views.detalle_factura, name='detalle'),
    path('generar/<int:venta_pk>/', views.generar_factura, name='generar'),
    path('<int:pk>/estado/', views.cambiar_estado, name='estado'),
]
