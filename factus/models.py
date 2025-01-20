from django.db import models

# Create your models here.

class Products(models.Model):
    name = models.CharField(max_length=50, )
    image = models.ImageField(upload_to='products', null=True, blank=True)
    price = models.IntegerField( )
    stock = models.IntegerField()

    def __str__(self):
        return f'{self.name} - {self.price} - {self.stock}'
    
    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'