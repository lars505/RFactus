from django.contrib import admin
from .models import Products, Category, Cart, CartProducts



admin.site.register(Products)
admin.site.register(Category)
admin.site.register(Cart)
admin.site.register(CartProducts)