from rest_framework import serializers

from product.models import Product, ProductImage, ProductCustomization
from users.serializers import ServiceLineSerializer, VendorSerializer


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = '__all__'


class ProductSerializer(serializers.Serializer):
    vendor = VendorSerializer()
    service_line = ServiceLineSerializer()
    images = serializers.SerializerMethodField('get_images')

    @staticmethod
    def get_images(obj):
        return ProductImageSerializer(ProductImage.objects.filter(product=obj), many=True).data

    class Meta:
        model = Product
        fields = '__all__'


class ProductCustomizationSerializer(serializers.Serializer):
    class Meta:
        model = ProductCustomization
        fields = '__all__'
