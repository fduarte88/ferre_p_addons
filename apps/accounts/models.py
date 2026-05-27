from django.db import models
from django.contrib.auth.models import User


class Perfil(models.Model):
    ROLES = [
        ('admin', 'Administrador'),
        ('vendedor', 'Vendedor'),
        ('bodeguero', 'Bodeguero'),
        ('contador', 'Contador'),
    ]
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    rol = models.CharField(max_length=20, choices=ROLES, default='vendedor')
    telefono = models.CharField(max_length=20, blank=True)
    activo = models.BooleanField(default=True)
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfiles'

    def __str__(self):
        return f'{self.usuario.get_full_name() or self.usuario.username} - {self.get_rol_display()}'
