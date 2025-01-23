from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect

from .models import Products, PaymentMethod, IdentificationDocumentType,Municipality, UnitMeasure

from django.views.decorators.csrf import csrf_exempt
import json

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
            data = json.loads(request.body)
            print(data)
            # # Procesar datos del cliente
            # cliente = data.get('cliente')
            # productos = data.get('productos')
            # subtotal = data.get('subtotal')
            # iva = data.get('iva')
            # total = data.get('total')
            
            # # Aquí puedes guardar los datos en tu base de datos o procesarlos
            # print("Datos del cliente:", cliente)
            # print("Productos:", productos)
            # print("Subtotal:", subtotal, "IVA:", iva, "Total:", total)

            # Responder al frontend
            return JsonResponse({'message': 'Factura procesada correctamente'}, status=200)
        
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    return JsonResponse({'error': 'Método no permitido'}, status=405)
