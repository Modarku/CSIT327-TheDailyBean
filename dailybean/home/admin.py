from django.contrib import admin
from .models import Product, ProductSubscription, Review

# Register models here
admin.site.register(Product)
admin.site.register(ProductSubscription)
admin.site.register(Review)

