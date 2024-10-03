from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100)
    total_rating = models.FloatField()
    imageurl = models.URLField(blank=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class Review(models.Model):
    productID = models.ForeignKey(Product, on_delete=models.CASCADE)
    text = models.TextField()
    rating = models.FloatField()