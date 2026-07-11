from django.contrib import admin
from .models import Proyecto, Tarea, Usuario
# Register your models here.

#Muestra tabla en el Dashboard
admin.site.register(Proyecto)
admin.site.register(Tarea)
admin.site.register(Usuario)