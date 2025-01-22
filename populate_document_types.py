import os
import django


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')  
django.setup()

from factus.models import IdentificationDocumentType  

def populate_document_types():
    document_types = [
        (1, "Registro civil"),
        (2, "Tarjeta de identidad"),
        (3, "Cédula ciudadanía"),
        (4, "Tarjeta de extranjería"),
        (5, "Cédula de extranjería"),
        (6, "NIT"),
        (7, "Pasaporte"),
        (8, "Documento de identificación extranjero"),
        (9, "PEP"),
        (10, "NIT otro país"),
        (11, "NUIP *"),
    ]

    for id, name in document_types:
        IdentificationDocumentType.objects.get_or_create(id=id, name=name)

if __name__ == "__main__":
    populate_document_types()
    print("¡Tipos de documentos poblados exitosamente!")
