from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages

from .models import Tarea, Proyecto, Usuario
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
    
def registro_view(request):
    # Vista para registrar usuarios utilizando el cifrado basado en matrices.
    if request.method == 'POST':
        correo = request.POST.get('correo')
        nombre = request.POST.get('nombre')
        password = request.POST.get('password')

        # Validación básica de seguridad
        if Usuario.objects.filter(correo_electronico=correo).exists():
            messages.error(request, "El correo ya está registrado en el sistema.")
            return redirect('registro')

        # Instanciación y guardado usando la función matemática
        nuevo_usuario = Usuario(
            correo_electronico=correo,
            nombre_completo=nombre
        )
        nuevo_usuario.set_password(password)
        nuevo_usuario.save()

        messages.success(request, "Usuario creado con éxito.")
        return redirect('login')

    return render(request, 'registro.html')

def login_view(request):
    # Vista de autenticación que evalúa la congruencia de los hashes.
    if request.method == 'POST':
        correo = request.POST.get('correo')
        password = request.POST.get('password')

        try:
            usuario = Usuario.objects.get(correo_electronico=correo)
            # Se aplica Algebra y Teoría de Números internamente en check_password
            if usuario.check_password(password):
                # Autenticación exitosa (Simulación de sesión)
                request.session['usuario_id'] = usuario.id_usuario
                return redirect('dashboard')
            else:
                messages.error(request, "Credenciales incorrectas.")
        except Usuario.DoesNotExist:
            messages.error(request, "El usuario no existe.")
            
    return render(request, 'login.html')

def logout_view(request):
    
    # Vista de control para finalizar la sesión del usuario.
    # Verificamos si existe una sesión activa antes de intentar cerrarla
    if 'usuario_id' in request.session:
        # flush() elimina todos los datos de la sesión y borra la cookie
        request.session.flush()
        messages.success(request, "Has cerrado sesión exitosamente. ¡Hasta pronto!")
    else:
        # Prevención de errores si un usuario no autenticado intenta acceder a la ruta
        messages.info(request, "No había ninguna sesión activa.")
        
    return redirect('login')