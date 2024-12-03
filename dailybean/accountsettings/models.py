from django.db import models
from login.models import User

# Create your models here.
class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    street_number = models.CharField(max_length=10)
    street = models.CharField(max_length=20)
    city = models.CharField(max_length=20)
    state = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=20)
    additional_details = models.CharField(max_length=255, blank=True, null=True)
    is_selected = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name}, {self.street_number} {self.street}, {self.city}, {self.country}"
