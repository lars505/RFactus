import os
import django

# Configurar el entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()  

from factus.models import UnitMeasure  

def populate_unit_measures():
    unit_measures = [
        {"id": 70, "code": "94", "name": "unidad"},
        {"id": 414, "code": "KGM", "name": "kilogramo"},
        {"id": 449, "code": "LBR", "name": "libra"},
        {"id": 512, "code": "MTR", "name": "metro"},
        {"id": 874, "code": "GLL", "name": "galón"},
    ]

    for unit in unit_measures:
        UnitMeasure.objects.get_or_create(
            id=unit["id"], 
            code=unit["code"], 
            name=unit["name"]
        )

if __name__ == "__main__":
    populate_unit_measures()
    print("¡Unidades de medida pobladas exitosamente!")
