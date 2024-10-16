from django.db import models

class Product(models.Model):
    product_name = models.CharField(max_length=255, null=False)
    product_description = models.CharField(max_length=255, null=False)
    product_ingredients = models.CharField(max_length=255, null=False)
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


class Review(models.Model):
    productID = models.ForeignKey(Product, on_delete=models.CASCADE)
    text = models.TextField()
    rating = models.FloatField()