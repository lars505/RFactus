from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect

from .models import Products, Category, Cart, CartProducts

def index(request):
    products = Products.objects.all()
    return render(request, 'factus/index.html',{'products': products})

def product_detail(request, product_id):
    product = Products.objects.get(id=product_id)
    return render(request, 'factus/product_detail.html', {'product': product})

def add_to_cart(request, product_id):
    product = get_object_or_404(Products, id= product_id)
    cantidad = request.POST.get('cantidad')

    #obtenemos el carrito
    cart, created = Cart.objects.get_or_create(user=request.user)

    #verificamos si el producto esta en el carrito
    try:
        cart_product = CartProducts.objects.get(cart = cart, product=product)
        cart_product.quantity += cantidad
        cart_product.save()
    except CartProducts.DoesNotExist:
        cart_product = CartProducts.objects.create(cart = cart, product=product, quantity=cantidad)

    return redirect('cart')


def cart(request):
    cart = Cart.objects.get(user=request.user)
    cart_products = CartProducts.objects.filter(cart=cart)
    return render(request, 'factus/carrito.html', {'cart': cart, 'cart_products': cart_products})
