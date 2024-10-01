from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from users.managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    class AppType(models.TextChoices):
        bazar = 'bazar'
        myket = 'myket'
        googleplay = 'googleplay'
        appstore = 'appstore'
        web = 'web'

    phone = models.CharField(max_length=20, null=False, blank=False, unique=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    image = models.ImageField(upload_to='user/image/', default=None, null=True)

    is_visible = models.BooleanField(default=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    is_vendor = models.BooleanField(default=False)

    date_joint = models.DateField(auto_now_add=True)

    app_type = models.CharField(default=AppType.bazar, choices=AppType.choices, max_length=20)
    version = models.CharField(default='0.0.0', max_length=20)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.phone


class ServiceLine(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    image = models.ImageField(upload_to='service_line/image/', default=None, null=True)

    def __str__(self):
        return self.name


class Country(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Address(models.Model):
    title = models.CharField(max_length=100, null=False, blank=False)
    address = models.CharField(max_length=100, null=False, blank=False)
    latitude = models.FloatField()
    longitude = models.FloatField()
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)
    postal_code = models.CharField(max_length=100, null=False, blank=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Vendor(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    service_line = models.ForeignKey(ServiceLine, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    image = models.ImageField(upload_to='vendor/image/', default=None, null=True)
    score = models.FloatField(default=0)

    is_active = models.BooleanField(default=True)
    start_hour = models.TimeField(null=True, default=None)
    end_hour = models.TimeField(null=True, default=None)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Customer(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='customer/image/', default=None, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.phone


class Wallet(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    balance = models.FloatField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.phone