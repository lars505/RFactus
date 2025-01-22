from django.contrib import admin
from .models import Products, IdentificationDocumentType, PaymentMethod, User



admin.site.register(Products)
admin.site.register(IdentificationDocumentType)
admin.site.register(PaymentMethod)
admin.site.register(User)