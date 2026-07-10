from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse

from .models import Tarea, Proyecto
from .forms import TareaForm, ProyectoForm

# Create your views here.
# Funcion auxiliar para verificar si el usuario es admin
def es_admin(user):
    return user.groups.filter(name='Admin').exists()

@login_required # Sino esta logueado, redirige a login

def dashboard(request):
    # Pasamos el usuario logueado a la vista del HTML
    es_admin = request.user.groups.filter(name='Admin').exists()  # Verifica si el usuario es superusuario o pertenece al grupo 'Admin'
    tareas = Tarea.objects.filter(asignada_a=request.user)  # Filtra las tareas asignadas al usuario logueado
    proyectos = Proyecto.objects.all()  # Obtiene todos los proyectos
    return render(request, 'dashboard.html', {'usuario': request.user, 'es_admin': es_admin, 'tareas': tareas, 'proyectos': proyectos})

@login_required
@user_passes_test(es_admin) # Solo los usuarios que pasen la prueba de la funcion es_admin podran acceder a esta vista
def crear_proyecto(request):

    if request.method == 'POST':
        #Se clica el boton "Guardar Proyecto"
        form = ProyectoForm(request.POST)
        if form.is_valid(): # Si el login es valido, se guarda el proyecto mediante un POST en la BD y luego redirige al dashboard
            form.save()
            return redirect('dashboard')
    else:
        form = ProyectoForm()
    return render(request, 'crear_proyecto.html', {'form':form})

@login_required
def crear_tarea(request):
    if request.method == 'POST':
        #Se clica el boton "Guardar Tarea"
        form = TareaForm(request.POST)
        if form.is_valid(): # Si el login es valido, se guarda la tarea mediante un POST en la BD y luego redirige al dashboard
            form.save()
            return redirect('dashboard')
    else:
        form = TareaForm()
    return render(request, 'crear_tarea.html', {'form':form})

def style(request):
    # Ruta para servir el archivo CSS
    return render(request, 'style.css', content_type='text/css')

def redirect_to(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        return redirect('login' )