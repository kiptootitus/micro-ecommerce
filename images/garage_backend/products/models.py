from django.db import models
from django.contrib.auth.models import User  # Import Django's built-in User model

class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='products/')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)  # Tracks who added the product
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
