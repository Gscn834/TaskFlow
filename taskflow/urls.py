from django.contrib import admin
from django.urls import path
from tareas import views as tareas_views # Importamos nuestras vistas de la aplicación tareas

urlpatterns = [
    # Rutas administrativas y de servicios
    path('admin/', admin.site.urls),
    path('style/', tareas_views.style, name='style'),  # Ruta para servir el archivo CSS

    # Rutas de autenticación
    path('login/', tareas_views.login_view, name='login'),
    path('logout/', tareas_views.logout_view, name='logout'),

    # Ruta para el registro de usuarios
    path('registro/', tareas_views.registro_view, name='registro'),
    
    # Ruta para el dashboard de tareas
    path('dashboard/', tareas_views.dashboard, name='dashboard'),

    # Rutas para crear actividades
    path('nueva_tarea/', tareas_views.crear_tarea, name='crear_tarea'),
    path('crear_proyecto/', tareas_views.crear_proyecto, name='crear_proyecto'),
    
    # Ruta de redireccion (Evita no page)
    path('', tareas_views.redirect_to, name='home'), # Ruta para redirigir a inicio o login
]