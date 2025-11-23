import os
import django
from django.contrib.auth.hashers import make_password

# Configura Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proyecto.settings')
django.setup()

from app2.models import User_admin

def registrar_usuario_console():
    print("Registro de Usuario Admin (por consola)")
    nombre = input("Nombre: ").strip()
    password = input("Contraseña: ").strip()
    email = input("Email (opcional): ").strip() or None
    telefono = input("Teléfono (opcional): ").strip() or None

    if not nombre or not password:
        print("Error: Nombre y contraseña son obligatorios.")
        return

    if User_admin.objects.filter(nombre=nombre).exists():
        print("Error: El nombre de usuario ya existe.")
        return

    if email and User_admin.objects.filter(email=email).exists():
        print("Error: El email ya está registrado.")
        return

    try:
        hashed_password = make_password(password)
        user = User_admin(
            nombre=nombre,
            password=hashed_password,
            email=email,
            telefono=telefono
        )
        user.save()
        print("Éxito: Usuario registrado correctamente.")
    except Exception as e:
        print(f"Error al registrar usuario: {e}")

if __name__ == '__main__':
    registrar_usuario_console()