# create_conserje_group.py
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from incidencias.models import Incidencia

def create_conserje_group():
    conserje_group, created = Group.objects.get_or_create(name='conserje')

    # Asignar permisos de lectura y escritura de incidencias al grupo conserje
    content_type = ContentType.objects.get_for_model(Incidencia)
    permissions = Permission.objects.filter(content_type=content_type)
    
    for perm in permissions:
        conserje_group.permissions.add(perm)

    print("Grupo conserje creado y permisos asignados.")

if __name__ == "__main__":
    create_conserje_group()
