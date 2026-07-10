from tkinter import CASCADE

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Proyecto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    fecha_creacion = models.DateField(auto_now_add=True)

# Proyecto muestra Nombre
    def __str__(self):
        return self.nombre

class Tarea(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True, null=True)
    completada = models.BooleanField(default=False)


    # Creacion de Relacion con Proyecto por llaves foraneas
    proyecto = models.ForeignKey('Proyecto', on_delete=models.CASCADE)
    asignada_a = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.titulo