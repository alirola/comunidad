from django.shortcuts import render, redirect
from .models import Incidencia
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import IncidenciaForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout
from .decorators import group_required
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import PermissionDenied

def crear_incidencia(request):
    if not request.user.is_superuser and not request.user.groups.filter(name='conserje').exists():
        if request.method == 'POST':
            form = IncidenciaForm(request.POST)
            if form.is_valid():
                incidencia = form.save(commit=False)
                incidencia.usuario = request.user
                incidencia.checks = request.POST.get('checks', {})
                incidencia.save()
                return redirect('crear_incidencia')
        else:
            form = IncidenciaForm() 
        return render(request, 'incidencias/crear_incidencia.html', {'form': form})
    else:
        raise PermissionDenied("No tienes permisos para acceder a esta página.")

@login_required
@user_passes_test(lambda u: u.groups.filter(name='conserje').exists() or u.is_superuser)
@login_required
def lista_incidencias(request):
    incidencias = Incidencia.objects.filter()
    return render(request, 'incidencias/lista_incidencias.html', {'incidencias': incidencias})

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('crear_incidencia')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            if user.is_superuser:
                return redirect('lista_incidencias')
            elif user.groups.filter(name='conserje').exists():
                return redirect('lista_incidencias')
            else:
                return redirect('crear_incidencia')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

@login_required
@user_passes_test(lambda u: u.is_superuser)
def superuser_dashboard(request):
    return render(request, 'dashboard/superuser_dashboard.html')

def logout_view(request):
    logout(request)
    return redirect('login')  # Redirige a la página de login después de cerrar sesión

@login_required
def procesar_incidencias(request):
    if request.method == 'POST':
        incidencias_ids = request.POST.getlist('incidencias')
        incidencias = Incidencia.objects.filter(usuario=request.user)
        for incidencia in incidencias:
            if str(incidencia.id) in incidencias_ids:
                incidencia.estado = True
            else:
                incidencia.estado = False
            incidencia.save()
        return redirect('lista_incidencias')
    return redirect('lista_incidencias')