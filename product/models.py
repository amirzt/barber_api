from django.db import models

from users.models import ServiceLine, Vendor


class Product(models.Model):
    class ProductType(models.TextChoices):
        shop = 'shop'
        home_service = 'home_service'
        salon_service = 'salon_service'

    type = models.CharField(max_length=100, choices=ProductType.choices, default=ProductType.shop)
    service_line = models.ForeignKey(ServiceLine, on_delete=models.SET_NULL, null=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    name = models.CharField(max_length=1000, null=False, blank=False)
    description = models.TextField(max_length=1000, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    stock = models.IntegerField(default=0)
    price = models.FloatField(default=0)
    score = models.FloatField(default=0)
    discount = models.FloatField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product/image/', default=None, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.name

class ProductCustomization(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=False, blank=False)
    price = models.FloatField(default=0)
    description = models.TextField(max_length=1000, null=True, blank=True)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name