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
                        "tax_rate": "19.00", 
                        "unit_measure_id": 70,  
                        "standard_code_id": 1, 
                        "is_excluded": 0,  
                        "tribute_id": 1, 
                        "withholding_taxes": [
                            {
                                "code": "01",  
                                "withholding_tax_rate": "15.00"
                            },
                        ] if producto.get("retenciones") else []
                    }
                    for producto in data.get("productos", [])
                ],
            }

          
            print("Datos enviados a la API:")
            print(json.dumps(factura_data, indent=4))

            response = api.request("POST", "/v1/bills/validate", data=factura_data)

            print(f"Respuesta de la API: {response}")

            return JsonResponse(response, safe=False)
        except Exception as e:
            print(f"Error en procesar_factura: {str(e)}")
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Método no permitido'}, status=405)

def load_facturas(request):
    api = FactusAPI()
    
    page = request.GET.get("page", 1)
    endpoint = f"/v1/bills?page={page}&filter[identification]&filter[names]&filter[number]&filter[prefix]&filter[reference_code]&filter[status]"
    
    # Realiza la solicitud al API
    response = api.request("GET", endpoint)
    
    if response["status"] == "OK":
        facturas = response["data"]["data"] 
        pagination = response["data"]["pagination"]  
    else:
        facturas = []
        pagination = None

    return render(request, "factus/facturas.html", {"facturas": facturas, "pagination": pagination})

def factura_info(request, number):
    api = FactusAPI()
    response = api.request("GET", f"/v1/bills/show/{number}")
    print(response)
    return render(request, "factus/factura_info.html", {"factura": response})


