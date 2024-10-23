from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Incidencia(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    estado = models.BooleanField(default=False)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    checks = models.JSONField(default=dict)

    def __str__(self):
        return self.titulo

class ReservaPadel(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()

    def __str__(self):
        return f"{self.usuario} - {self.fecha} de {self.hora_inicio} a {self.hora_fin}"
    
    class Meta:
        unique_together = ['fecha', 'hora_inicio', 'hora_fin']