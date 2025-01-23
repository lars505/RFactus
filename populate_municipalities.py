import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from factus.models import Municipality 

# Ruta del archivo JSON
JSON_FILE_PATH = 'municipalities.json'

def populate_municipalities():
    # Leer el archivo JSON
    try:
        with open(JSON_FILE_PATH, 'r', encoding='utf-8') as file:
            municipality_data = json.load(file)
    except FileNotFoundError:
        print(f"Error: El archivo '{JSON_FILE_PATH}' no existe.")
        return
    except json.JSONDecodeError:
        print("Error: El archivo JSON tiene un formato incorrecto.")
        return

    # Insertar los datos en la base de datos
    for data in municipality_data:
        municipality, created = Municipality.objects.get_or_create(
            id=data["id"],
            code=data["code"],
            name=data["name"],
            department=data["department"],
        )
        if created:
            print(f"Municipality '{municipality.name}' created.")
        else:
            print(f"Municipality '{municipality.name}' already exists.")

if __name__ == "__main__":
    populate_municipalities()
