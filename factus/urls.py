from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),  
    path('product-detail/<int:product_id>/',views.product_detail, name='product_detail'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
]
