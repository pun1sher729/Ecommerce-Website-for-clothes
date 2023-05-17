from django.contrib import admin
from .models import *

admin.site.register(customer)
admin.site.register(seller)
admin.site.register(product)
admin.site.register(cart)

# Register your models here.
