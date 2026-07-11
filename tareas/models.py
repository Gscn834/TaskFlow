from django.db import models 
from .crypto_math import math_custom_hash, verify_password

class Usuario(models.Model):
    
    # Modelo de datos relacional para la tabla de usuarios en MySQL.
    id_usuario = models.AutoField(primary_key=True)
    correo_electronico = models.EmailField(unique=True, max_length=150)
    nombre_completo = models.CharField(max_length=200)
    password_hash = models.CharField(max_length=256)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'usuarios_taskflow'

    def set_password(self, raw_password):
        # Asigna la contraseña aplicando el algoritmo matemático.
        self.password_hash = math_custom_hash(raw_password)

    def check_password(self, raw_password):
        # Verifica la contraseña ingresada.
        return verify_password(raw_password, self.password_hash)

    def __str__(self):
        return f"{self.nombre_completo} ({self.correo_electronico})"

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
    asignada_a = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    def __str__(self):
        return self.titulo