from django.db import models

from product.models import Product, ProductCustomization
from users.models import CustomUser, Address


class Order(models.Model):
    class OrderStatus(models.TextChoices):
        PENDING = 'pending', 'Pending'
        PROCESSING = 'processing', 'Processing'
        SHIPPED = 'shipped', 'Shipped'
        DELIVERED = 'delivered', 'Delivered'
        CANCELLED = 'cancelled', 'Cancelled'

    class PaymentMethod(models.TextChoices):
        CASH = 'cash', 'Cash'
        ONLINE = 'online', 'Online'

    class ProductType(models.TextChoices):
        SHOP = 'shop', 'Shop'
        HOME_SERVICE = 'home_service', 'Home Service'
        SALON_SERVICE = 'salon_service', 'Salon Service'

    product_type = models.CharField(max_length=100, choices=ProductType.choices, default=ProductType.SHOP)
    payment_method = models.CharField(max_length=100, choices=PaymentMethod.choices, default=PaymentMethod.CASH)
    status = models.CharField(max_length=100, choices=OrderStatus.choices, default=OrderStatus.PENDING)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    date = models.DateField()
    time = models.TimeField()

    price = models.FloatField(default=0)
    discount = models.FloatField(default=0)

    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    customization = models.ForeignKey(ProductCustomization, on_delete=models.SET_NULL, null=True)

    quantity = models.IntegerField(default=1)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
