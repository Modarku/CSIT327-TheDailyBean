from django.db import models
from login.models import User
from django.utils import timezone
from datetime import datetime

class Product(models.Model):
    product_name = models.CharField(max_length=255, null=False)
    product_description = models.TextField(null=False)  
    product_ingredients = models.TextField(null=False)
    product_shelflife = models.CharField(max_length=255, null=False)
    product_image = models.ImageField(upload_to='products/', null=False)
    rating = models.FloatField()
    stock = models.IntegerField(null=False, default=0)
    is_available = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=5, decimal_places=2, null=False, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.product_name
    
    def save(self, *args, **kwargs):
        self.rating = 0
        if self.stock > 0:
            self.is_available = True
        else:
            self.is_available = False
        super(Product, self).save(*args, **kwargs)

class ProductSubscription(models.Model):
    ONEBEAN = 'onebean'
    WEEKLYBEAN = 'weeklybean'
    CHOICEBEAN = 'choicebean'

    SUBSCRIPTION_TYPE_CHOICES = [
        (ONEBEAN, 'Onebean'),
        (WEEKLYBEAN, 'Weeklybean'),
        (CHOICEBEAN, 'Choicebean'),
    ]


    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    subscription_type = models.CharField(max_length=10, choices=SUBSCRIPTION_TYPE_CHOICES)
    next_monthly = models.DateTimeField(default=None)
    is_active = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=5, decimal_places=2, null=False, default=0)

    def __str__(self):
        return self.subscription_type + " Product: " + self.product.product_name + " User: " + self.user.username
    


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    text = models.TextField()
    rating = models.FloatField()
    date_created = models.DateTimeField(default=timezone.now)