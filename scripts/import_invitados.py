import os
from pathlib import Path

# Configura Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proyecto.settings')
import django
django.setup()

from app1.models import Invitado

def normalize_name(line: str) -> str:
    return " ".join(line.strip().split())

def split_name(full_name: str):
    parts = full_name.split()
    if not parts:
        return None, None
    if len(parts) == 1:
        return parts[0], None
    return parts[0], " ".join(parts[1:])

def import_from_file(file_path: Path):
    if not file_path.exists():
        print(f"Archivo no encontrado: {file_path}")
        return

    seen = set()
    created = []
    skipped = []

    with file_path.open(encoding='utf-8') as f:
        for raw in f:
            name = normalize_name(raw)
            if not name:
                continue
            key = name.lower()
            if key in seen:
                skipped.append((name, 'duplicado en archivo'))
                continue
            seen.add(key)

            nombre, apellido = split_name(name)
            # Normalizar None vs empty string for comparison
            lookup_kwargs = {'nombre__iexact': nombre}
            if apellido:
                lookup_kwargs['apellido__iexact'] = apellido
            else:
                lookup_kwargs['apellido__isnull'] = True

            exists = Invitado.objects.filter(**lookup_kwargs).exists()
            if exists:
                skipped.append((name, 'ya en DB'))
                continue

            invitado, created_flag = Invitado.objects.get_or_create(
                nombre=nombre,
                apellido=apellido if apellido else None
            )
            if created_flag:
                created.append(name)
            else:
                skipped.append((name, 'ya en DB (get_or_create)'))

    # Resumen
    print(f"Procesado: {len(seen)} nombres únicos encontrados en el archivo.")
    print(f"Creados: {len(created)}")
    if created:
        print("Lista de creados (primeros 20):")
        for n in created[:20]:
            print("  -", n)
    print(f"Omitidos: {len(skipped)}")
    if skipped:
        print("Ejemplos de omitidos (primeros 20):")
        for n, reason in skipped[:20]:
            print(f"  - {n}  ({reason})")

if __name__ == '__main__':
    BASE_DIR = Path(__file__).resolve().parent.parent
    invitados_file = BASE_DIR / 'Invitados.txt'
    import_from_file(invitados_file)
