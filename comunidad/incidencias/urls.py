from django.urls import path 
from . import views

urlpatterns = [
	path('', views.lista_incidencias, name='lista_incidencias'),
	path('crear/', views.crear_incidencia, name='crear_incidencia'),
]