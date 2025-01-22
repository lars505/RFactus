from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),  
    path('product/',views.product, name='products'),
    path('fact',views.factura, name='facturacion'),
]
