from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from product.models import Product
from product.serializers import ProductSerializer
from users.models import CustomUser, Vendor


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def product(request):
    user = CustomUser.objects.get(id=request.user.id)

    if user.is_vendor:
        vendor = Vendor.objects.get(user=user)
        products = Product.objects.filter(vendor=vendor)
    else:
        products = Product.objects.filter(is_active=True)

    if 'vendor' in request.data:
        products = products.filter(vendor_id=request.data['vendor'])
    if 'service_line' in request.data:
        products = products.filter(service_line=request.data['service_line'])
    if 'type' in request.data:
        products = products.filter(type=request.data['type'])
    return Response(ProductSerializer(products, many=True).data)