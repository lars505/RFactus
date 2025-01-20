from django.conf import settings
from django.shortcuts import render
from .models import Products

# Create your views here.

def index(request):

    return render(request, 'factus/index.html')