from django.core.serializers import serialize
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from product.models import Product, ProductImage, ProductCustomization
from product.serializers import ProductSerializer, AddProductSerializer, ProductImageSerializer, \
    ProductCustomizationSerializer
from users.models import CustomUser, Vendor, ServiceLine


@api_view(['GET'])
@permission_classes([AllowAny])
def get_product(request):
    if request.user.is_authenticated:
        user = CustomUser.objects.get(id=request.user.id)
        if user.is_vendor:
            vendor = Vendor.objects.get(user=user)
            products = Product.objects.filter(vendor=vendor)
        else:
            products = Product.objects.filter(is_active=True)
    else:
        products = Product.objects.filter(is_active=True)

    if 'vendor' in request.query_params:
        products = products.filter(vendor_id=request.query_params.get('vendor'))
    if 'service_line' in request.query_params:
        products = products.filter(service_line_id=request.query_params.get('service_line'))
    if 'type' in request.query_params:
        products = products.filter(type=request.query_params.get('type'))
    if 'sort' in request.query_params:
        products = products.order_by(request.query_params.get('sort'))
    if 'search' in request.query_params:
        products = products.filter(name__contains=request.query_params.get('search'))
    return Response(ProductSerializer(products, many=True).data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_product(request):
    user = CustomUser.objects.get(id=request.user.id)
    vendor = Vendor.objects.get(user=user)

    serializer = AddProductSerializer(data=request.data, context={'vendor': vendor})
    if serializer.is_valid():
        product = serializer.save()
        return Response({"product_id": product.id}, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_product(request):
    product = Product.objects.get(id=request.data['id'])

    if 'is_active' in request.data:
        product.is_active = request.data['is_active']
    if 'name' in request.data:
        product.name = request.data['name']
    if 'description' in request.data:
        product.description = request.data['description']
    if 'price' in request.data:
        product.price = request.data['price']
    if 'discount' in request.data:
        product.discount = request.data['discount']
    if 'service_line' in request.data:
        product.service_line = ServiceLine.objects.get(id=request.data['service_line'])
    if 'type' in request.data:
        product.type = request.data['type']
    if 'stock' in request.data:
        product.stock = request.data['stock']

    product.save()
    return Response(status=status.HTTP_200_OK)


@api_view(['POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def product_image(request):
    if request.method == 'POST':
        serializer = ProductImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        image = ProductImage.objects.get(id=request.data['id'])
        image.delete()
        return Response(status=status.HTTP_200_OK)


@api_view(['POST', 'GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def customization(request):
    user = CustomUser.objects.get(id=request.user.id)
    if request.method == 'POST':
        serializer = ProductCustomizationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'GET':
        customs = ProductCustomization.objects.filter(product_id=request.query_params['product'])
        if not user.is_vendor:
            customs = customs.filter(is_active=True)
        return Response(ProductCustomizationSerializer(customs, many=True).data)

    elif request.method == 'PUT':
        custom = ProductCustomization.objects.get(id=request.data['id'])
        if 'price' in request.data:
            custom.price = request.data['price']
        if 'name' in request.data:
            custom.name = request.data['name']
        if 'is_active' in request.data:
            custom.is_active = request.data['is_active']
        custom.save()
        return Response(status=status.HTTP_200_OK)
    elif request.method == 'DELETE':
        custom = ProductCustomization.objects.get(id=request.data['id'])
        custom.delete()
        return Response(status=status.HTTP_200_OK)