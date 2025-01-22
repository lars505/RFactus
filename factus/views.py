from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect

from .models import Products, PaymentMethod, IdentificationDocumentType

def index(request):
    return render(request, 'factus/index.html')

def product(request):
   
    if request.method == 'POST':
        nombre = request.POST['name']
        precio = request.POST['price']
        descripcion = request.POST['description']
        stock = request.POST['stock']
        imagen = request.FILES['image']

        producto = Products.objects.create(
            name=nombre,
            price=precio,
            description=descripcion,
            stock=stock,
            image=imagen
        )
        producto.save()
    
    products = Products.objects.all()
    return render(request, 'factus/producto.html', {'products': products})

def factura(request):
    return render(request,'factus/facturacion.html')

def load_factura(request):
    products = list(Products.objects.all().values('id', 'name', 'price', 'stock'))
    document_types = list(IdentificationDocumentType.objects.all().values('id', 'name'))    
    payment_methods = list(PaymentMethod.objects.all().values('code', 'description'))
    return JsonResponse({
        'products': products,
        'document_types': document_types,
        'payment_methods': payment_methods,
    })