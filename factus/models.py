from django.db import models
from django.contrib.auth.models import User, AbstractUser


class User(AbstractUser):
    pass


class IdentificationDocumentType(models.Model):
    id = models.PositiveIntegerField(primary_key=True)  
    name = models.CharField(max_length=100) 

    def __str__(self):
        return self.name

    def serialize(self):
        return {
            'id':self.id,
            'name':self.name,
        }

class UnitMeasure(models.Model):
    code = models.CharField(max_length=10, unique=True)  
    name = models.CharField(max_length=100) 

    def serialize(self):
        return {
            'code':self.code,
            'name':self.name,
        }
    def __str__(self):
        return f"{self.name} ({self.code})"

class Products(models.Model):
    name = models.CharField(max_length=50, )
    image = models.ImageField(upload_to='products', null=True, blank=True)
    description = models.TextField( blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    unit_measure = models.ForeignKey(UnitMeasure, on_delete=models.CASCADE, null=True, blank=True)

    def serialize(self):
        return {
            'id':self.id,
            'name':self.name,
            'image':self.image.url,
            'price':self.price,
            'stock':self.stock,          
           
        }


    def __str__(self):
        return f'{self.name} - {self.price} - {self.stock}'
    
    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'


class PaymentMethod(models.Model):
    code = models.CharField(max_length=10, primary_key=True)
    description = models.CharField(max_length=255) 
    
    def serialize(self):
        return {
            'code':self.code,
            'description':self.description,
        }

    def __str__(self):
        return f"{self.code} - {self.description}"
    

    

class Municipality(models.Model): # ID único
    code = models.CharField(max_length=10, unique=True) 
    name = models.CharField(max_length=100)
    department = models.CharField(max_length=100) 

    def serialize(self):
        return {
            'id':self.id,
            'code':self.code,
            'name':self.name,
            'department':self.department,
        }

    def __str__(self):
        return f"{self.name}, {self.department} ({self.code})"
