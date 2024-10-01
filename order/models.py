from django.db import models

from product.models import Product, ProductCustomization
from users.models import CustomUser, Address, Vendor


class Order(models.Model):
    class OrderStatus(models.TextChoices):
        PENDING = 'pending', 'Pending'
        ACCEPTING = 'accepting', 'Accepting'
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
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)

    date = models.DateField(null=True)
    time = models.TimeField(null=True)

    price = models.FloatField(default=0)
    discount = models.FloatField(default=0)

    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True)

    user_description = models.TextField(max_length=1000, null=True, blank=True)
    vendor_description = models.TextField(max_length=1000, null=True, blank=True)
    admin_description = models.TextField(max_length=1000, null=True, blank=True)


    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.user.phone


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    customization = models.ForeignKey(ProductCustomization, on_delete=models.SET_NULL, null=True)
    price = models.FloatField(default=0)

    quantity = models.IntegerField(default=1)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.product.name


class Comment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField(max_length=1000, null=False, blank=False)
    rating = models.FloatField(default=0)
    reply = models.TextField(max_length=1000, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Transaction(models.Model):
    class PaymentMethod(models.TextChoices):
        PAYPAL = 'paypal', 'Paypal'

    class PaymentStatus(models.TextChoices):
        PENDING = 'pending', 'Pending'
        SUCCESS = 'success', 'Success'
        FAILED = 'failed', 'Failed'


    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=100, choices=PaymentMethod.choices, default=PaymentMethod.PAYPAL)
    payment_status = models.CharField(max_length=100, choices=PaymentStatus.choices, default=PaymentStatus.PENDING)

    income = models.BooleanField(default=True)
    tracking_code = models.CharField(max_length=100, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
