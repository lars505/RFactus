from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect

from .models import Products, Category, Cart, CartProducts

def index(request):
    products = Products.objects.all()
    return render(request, 'factus/index.html',{'products': products})


def product_detail(request, product_id):
    product = Products.objects.get(id=product_id)
    return render(request, 'factus/product_detail.html', {'product': product})



#carrito

def add_to_cart(request, product_id):
    product = get_object_or_404(Products, id= product_id)

    print(product)

    cart, created = Cart.objects.get_or_create(user=request.user, total=0.00)

    cart_product, created = CartProducts.objects.get_or_create(cart=cart, product=product)
    
    if not created:
        cart_product.quantity += 1
        cart_product.save()

    else:
        cart_product.quantity = 1
        cart_product.save()


    cart.total = sum(item.product.price * item.quantity for item in cart.cartproducts.all())
    cart.IVA = cart.total * 0.16
    cart.save()

    return redirect('detalle_carrito')
