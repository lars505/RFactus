from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),  
    path('product/',views.product, name='products'),
    path('fact/',views.factura, name='facturacion'),
    path('load_data/',views.load_data, name='load_data'),
    path('load_product/<int:product_id>/',views.load_product, name='load_product'),
    path('procesar_factura/', views.procesar_factura, name='procesar_factura'),
]
