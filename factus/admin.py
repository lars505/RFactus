from django.contrib import admin
from .models import Products, IdentificationDocumentType, PaymentMethod, User, Municipality, UnitMeasure



admin.site.register(Products)
admin.site.register(IdentificationDocumentType)
admin.site.register(PaymentMethod)
admin.site.register(User)
admin.site.register(Municipality)
admin.site.register(UnitMeasure)