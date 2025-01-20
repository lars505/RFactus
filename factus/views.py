from django.conf import settings
from django.urls import reverse
from django.http import JsonResponse
from django.shortcuts import render, HttpResponseRedirect

from .models import Products, Category



def index(request):

    products = Products.objects.all()

    return render (request, 'partials/htmx-components/product_list.html',{'products': products})


