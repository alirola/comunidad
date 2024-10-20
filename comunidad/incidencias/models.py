from django.db import models
from django.contrib.auth.models import User

class Incidencia(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    estado = models.BooleanField(default=False)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    checks = models.JSONField(default=dict)

    def __str__(self):
        return self.titulo