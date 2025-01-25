import json
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from .models import Products, PaymentMethod, IdentificationDocumentType,Municipality, UnitMeasure

import uuid


from .services.factus_api import FactusAPI

def index(request):
    return render(request, 'factus/index.html')

def product(request):
   
    if request.method == 'POST':
        nombre = request.POST['name']
        precio = request.POST['price']
        descripcion = request.POST['description']
        stock = request.POST['stock']
        imagen = request.FILES['image']
        unidad = request.POST['unidad']

        unitmeasure = UnitMeasure.objects.get(pk=unidad)

        producto = Products.objects.create(
            name=nombre,
            price=precio,
            description=descripcion,
            stock=stock,
            image=imagen,
            unit_measure=unitmeasure

        )
        producto.save()
    
    products = Products.objects.all()
    unitmeasure = UnitMeasure.objects.all()
    return render(request, 'factus/producto.html', {'products': products, 'unitmeasure': unitmeasure})

def factura(request):
    return render(request,'factus/facturacion.html')

def load_data(request):
    
    products = Products.objects.all()
    document_types = IdentificationDocumentType.objects.all() 
    payment_methods = PaymentMethod.objects.all()[:10]
    municipality = Municipality.objects.all()

    return JsonResponse({
        'products': [product.serialize() for product in products],
        'document_types': [document_type.serialize() for document_type in document_types ],
        'payment_methods': [payment_method.serialize() for payment_method in payment_methods],
        'municipality': [municipalities.serialize() for municipalities in municipality]
    })

def load_product(request, product_id):
    product = get_object_or_404(Products, pk=product_id)
    return JsonResponse(product.serialize())

@csrf_exempt
def procesar_factura(request):
    if request.method == 'POST':
        try:
            try:
                data = json.loads(request.body)
            except json.JSONDecodeError:
                return JsonResponse({'error': 'Formato JSON inválido'}, status=400)

            api = FactusAPI()

            factura_data = {
                "numbering_range_id": data.get("rango"),
                "reference_code": f"Fact-{uuid.uuid4()}" ,
                "observation": "",
                "payment_form": "1",
                "payment_method_code": data["cliente"].get("metodoPago", "10"),        
                "customer": {
                    "identification": data["cliente"].get("identificacion"),
                    "dv": data["cliente"].get("dv", "3"),
                    "company": "",
                    "trade_name": "",
                    "names": data["cliente"].get("nombre"),
                    "address": data["cliente"].get("direccion"),
                    "email": data["cliente"].get("email"),
                    "phone": data["cliente"].get("telefono"),
                    "legal_organization_id": data["cliente"].get("tipoCliente"),
                    "tribute_id": "21",
                    "identification_document_id": data["cliente"].get("tipoIdentificacion"),
                    "municipality_id": data["cliente"].get("municipio"),
                },
                "items": [
                    {
                        "code_reference": str(producto["data"].get("id")),
                        "name": producto["data"].get("name"),
                        "quantity": producto.get("cantidad"),
                        
                        "discount_rate": producto.get("descuento", 0),
                        "price": str(producto["data"].get("price")),
                        "tax_rate": "19.00",  # Ajusta según sea necesario
                        "unit_measure_id": 70,  # Ajusta si es necesario
                        "standard_code_id": 1,  # Ajusta si es necesario
                        "is_excluded": 0,  # Cambiar si el producto está excluido de IVA
                        "tribute_id": 1,  # Cambiar si es necesario
                        "withholding_taxes": [
                            {
                                "code": "01",  # Ajusta según sea necesario
                                "withholding_tax_rate": "19.00"
                            },
                        ] if producto.get("retenciones") else []
                    }
                    for producto in data.get("productos", [])
                ],
            }

            # Depuración: Ver datos de la factura
            print("Datos enviados a la API:")
            print(json.dumps(factura_data, indent=4))

            # Solicitud a la API
            response = api.request("POST", "/v1/bills/validate", data=factura_data)

            # Verificar si la respuesta es válida
            return JsonResponse(response, safe=False)
        except Exception as e:
            print(f"Error en procesar_factura: {str(e)}")
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Método no permitido'}, status=405)


# def load_facturas(request):
#     api = FactusAPI()
    
#     # Obtén la página actual desde los parámetros GET (por defecto, es la página 1)
#     page = request.GET.get("page", 1)
#     endpoint = f"/v1/bills?page={page}&filter[identification]&filter[names]&filter[number]&filter[prefix]&filter[reference_code]&filter[status]"
    
#     # Realiza la solicitud al API
#     response = api.request("GET", endpoint)
    
#     if response["status"] == "OK":
#         facturas = response["data"]["data"]  # Lista de facturas
#         pagination = response["data"]["pagination"]  # Datos de paginación
        
#         for factura in facturas:
#             # print(factura["id"])
#             detalle_factura = api.request("GET", f"/v1/bills/show/{factura['number']}")
#             factura["dian"] = detalle_factura.get('data', '').get('bill', '').get('qr', '')
#             factura["factura"] = detalle_factura.get('data', '').get('bill', '').get('public_url', '')
#     else:
#         facturas = []
#         pagination = None

#     return render(request, "factus/facturas.html", {"facturas": facturas, "pagination": pagination})

import concurrent.futures

def obtener_detalle_factura(factura):
    api = FactusAPI()
    return api.request("GET", f"/v1/bills/show/{factura['number']}")

def load_facturas(request):
    api = FactusAPI()
    page = request.GET.get("page", 1)
    endpoint = f"/v1/bills?page={page}&filter[identification]&filter[names]&filter[number]&filter[prefix]&filter[reference_code]&filter[status]"
    
    response = api.request("GET", endpoint)
    
    if response["status"] == "OK":
        facturas = response["data"]["data"]
        pagination = response["data"]["pagination"]
        
        # Realizamos las solicitudes de forma concurrente
        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = list(executor.map(obtener_detalle_factura, facturas))
        
        # Asignamos los resultados a las facturas
        for factura, detalle_factura in zip(facturas, results):
            factura["dian"] = detalle_factura.get('data', {}).get('bill', {}).get('qr', '')
            factura["factura"] = detalle_factura.get('data', {}).get('bill', {}).get('public_url', '')
            
    else:
        facturas = []
        pagination = None

    return render(request, "factus/facturas.html", {"facturas": facturas, "pagination": pagination})

def factura_info(request, number):
    api = FactusAPI()
    response = api.request("GET", f"/v1/bills/show/{number}")
    return JsonResponse(response)


