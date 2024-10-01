from django.contrib import admin

from order.models import Order, OrderProduct, Comment, Transaction


# Register your models here.
@admin.register(Order)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('user', 'vendor', 'status', 'created_at', 'updated_at')
    search_fields = ('user__phone', 'user__name', 'vendor__name')
    fields = (
    'user', 'vendor', 'product_type', 'payment_method', 'status', 'price', 'date', 'time', 'discount', 'address',
    'user_description', 'vendor_description', 'admin_description')


@admin.register(OrderProduct)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'created_at', 'updated_at')
    search_fields = ('product__name',)
    fields = ('order', 'product', 'customization', 'quantity', 'price')


@admin.register(Comment)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('order', 'user', 'created_at', 'updated_at')
    # search_fields = ('product__name',)
    fields = ('order', 'vendor', 'user', 'content', 'rating', 'reply')


@admin.register(Transaction)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('order', 'payment_status', 'created_at', 'updated_at')
    # search_fields = ('product__name',)
    fields = ('order', 'payment_method', 'payment_status', 'income', 'tracking_code')