from django.db import models
from home.models import Product
from login.models import User

class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=7, decimal_places=2)
    product_amount = models.PositiveSmallIntegerField()
    date_paid = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"