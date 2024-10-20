"""
URL configuration for comunidad project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from incidencias import views as incidencias_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('crear_incidencia/', incidencias_views.crear_incidencia, name='crear_incidencia'),
    path('lista_incidencias/', incidencias_views.lista_incidencias, name='lista_incidencias'),
    path('accounts/login/', incidencias_views.login_view, name='login'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('signup/', incidencias_views.signup, name='signup'),
    path('', incidencias_views.login_view, name='default_view'),
    path('superuser_dashboard/', incidencias_views.superuser_dashboard, name='superuser_dashboard'),
    path('accounts/logout/', incidencias_views.logout, name='logout'),
    path('procesar_incidencias/', incidencias_views.procesar_incidencias, name='procesar_incidencias'),
]
