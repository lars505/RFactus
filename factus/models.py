from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=25)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"


class Products(models.Model):
    name = models.CharField(max_length=50, )
    image = models.ImageField(upload_to='products', null=True, blank=True)
    descriotion = models.TextField( blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")

    def serialize(self):
        return {
            'id':self.id,
            'name':self.name,
            'image':self.image.url,
            'price':self.price,
            'stock':self.stock,
            'category': {
                'id': self.category.id,
                'name': self.category.name
            } if self.category else None 
          
        }


    def __str__(self):
        return f'{self.name} - {self.price} - {self.stock}'
    
    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'


class Cart(models.Model):
    products = models.ManyToManyField(Products, through='CartProducts')
    descuento = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    IVA = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f'Carrito: {self.id}'

    class Meta:
        verbose_name = 'Carrito'
        verbose_name_plural = 'Carritos'


class CartProducts(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)  # Aquí puedes añadir más campos como la cantidad.

    def __str__(self):
        return f'{self.quantity} x {self.product.name} in Cart {self.cart.id}'
