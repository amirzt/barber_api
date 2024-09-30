from django.contrib import admin

from product.models import Product, ProductImage, ProductCustomization


# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'vendor','created_at', 'updated_at')
    search_fields = ('name',)
    fields = ('name', 'vendor', 'service_line', 'type', 'description', 'is_active', 'stock', 'price', 'discount')


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'image', 'created_at', 'updated_at')
    search_fields = ('product__name',)
    fields = ('product', 'image')


@admin.register(ProductCustomization)
class ProductCustomizationAdmin(admin.ModelAdmin):
    list_display = ('product', 'name', 'price', 'description', 'is_active', 'created_at', 'updated_at')
    search_fields = ('name',)
    fields = ('product', 'name', 'price', 'description', 'is_active')
