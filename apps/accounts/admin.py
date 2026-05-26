from django.contrib import admin
from .models import Perfil


@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'rol', 'telefono', 'activo', 'creado')
    list_filter = ('rol', 'activo')
    search_fields = ('usuario__username', 'usuario__first_name', 'usuario__last_name')
