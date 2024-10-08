from rest_framework import serializers

from product.models import Product, ProductImage, ProductCustomization
from users.serializers import ServiceLineSerializer, VendorSerializer


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = '__all__'
    def save(self, **kwargs):
        image = ProductImage(product=self.validated_data.get('product'),
                             image=self.validated_data['image'])
        image.save()
        return image


class ProductSerializer(serializers.ModelSerializer):
    vendor = VendorSerializer()
    service_line = ServiceLineSerializer()
    images = serializers.SerializerMethodField('get_images')
    customizations = serializers.SerializerMethodField('get_customizations')

    @staticmethod
    def get_images(obj):
        return ProductImageSerializer(ProductImage.objects.filter(product=obj), many=True).data

    @staticmethod
    def get_customizations(obj):
        return ProductCustomizationSerializer(ProductCustomization.objects.filter(product=obj), many=True).data

    class Meta:
        model = Product
        fields = '__all__'


class AddProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['service_line', 'name', 'description', 'type', 'price', 'stock', 'discount']

    def save(self, **kwargs):
        product = Product(service_line=self.validated_data['service_line'],
                          vendor=self.context.get('vendor'),
                          name=self.validated_data['name'],
                          description=self.validated_data['description'],
                          type=self.validated_data['type'],
                          price=self.validated_data['price'],
                          stock=self.validated_data['stock'],
                          discount=self.validated_data['discount'])
        product.save()
        return product

class ProductCustomizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCustomization
        fields = '__all__'

    def save(self, **kwargs):
        customization = ProductCustomization(product=self.validated_data.get('product'),
                                             name=self.validated_data['name'],
                                             price=self.validated_data['price'],
                                             description=self.validated_data['description'])
        customization.save()
        return customization
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.price = validated_data.get('price', instance.price)
        instance.description = validated_data.get('description', instance.description)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.save()
        return instance
