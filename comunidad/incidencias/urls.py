from django.urls import path 
from . import views

urlpatterns = [
	path('', views.pagina_principal, name='pagina_principal'),
	path('crear/', views.crear_incidencia, name='crear_incidencia'),
	path('horarios/', views.ver_horarios, name='ver_horarios'),
    path('reservar/', views.reservar_pista, name='reservar_pista'),
	path('pista/horarios/', views.ver_horarios, name='ver_horarios'),
]