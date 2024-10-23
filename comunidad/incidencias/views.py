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
from django.core.mail import send_mail
from django.conf import settings
from .models import ReservaPadel
from .forms import ReservaPadelForm
from django.contrib import messages

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

@login_required
def ver_horarios(request):
    reservas = ReservaPadel.objects.all().order_by('fecha', 'hora_inicio')
    return render(request, 'pistas/ver_horarios.html', {'reservas': reservas})

@login_required
def reservar_pista(request):
    if request.method == 'POST':
        form = ReservaPadelForm(request.POST)
        if form.is_valid():
            # Verificar si ya existe una reserva en ese horario
            fecha = form.cleaned_data['fecha']
            hora_inicio = form.cleaned_data['hora_inicio']
            hora_fin = form.cleaned_data['hora_fin']

            conflicto = ReservaPadel.objects.filter(fecha=fecha, hora_inicio__lt=hora_fin, hora_fin__gt=hora_inicio).exists()

            if conflicto:
                messages.error(request, "Ya existe una reserva en este horario.")
            else:
                reserva = form.save(commit=False)
                reserva.usuario = request.user
                reserva.save()
                messages.success(request, "Reserva realizada con éxito.")
                return redirect('ver_horarios')
    else:
        form = ReservaPadelForm()

    return render(request, 'pistas/reservar_pista.html', {'form': form})

@login_required
def pagina_principal(request):
        return render(request, 'pagina_principal.html')