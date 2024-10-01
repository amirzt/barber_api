from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from order.models import Order, OrderProduct, Comment
from order.serializers import AddOrderSerializer, AddOrderProductSerializer, OrderSerializer, AddCommentSerializer
from users.models import CustomUser, Vendor, Address


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_order(request):
    user = CustomUser.objects.get(id=request.user.id)
    vendor = Vendor.objects.get(id=request.data['vendor'])

    try:
        order = Order.objects.get(user=user,
                                  vendor=vendor,
                                  status=Order.OrderStatus.PENDING)
    except Order.DoesNotExist:
        serializer = AddOrderSerializer(data=request.data,
                                        context={'user': user})
        if serializer.is_valid():
            order = serializer.save()
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    product_serializer = AddOrderProductSerializer(data=request.data['products'],
                                               context={'order': order})
    if product_serializer.is_valid():
        product = product_serializer.save()
        order.price = order.price + product.price
        order.product_type = product.product.type
        order.save()
        return Response(status=status.HTTP_200_OK)
    else:
        return Response(product_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_order(request):
    order = Order.objects.get(id=request.data['id'])

    if 'status' in request.data:
        order.status = request.data['status']
    if 'user_description' in request.data:
        order.user_description = request.data['user_description']
    if 'vendor_description' in request.data:
        order.vendor_description = request.data['vendor_description']
    if 'admin_description' in request.data:
        order.admin_description = request.data['admin_description']
    if 'payment_method' in request.data:
        order.payment_method = request.data['payment_method']
    if 'date' in request.data:
        order.date = request.data['date']
    if 'time' in request.data:
        order.time = request.data['time']
    if 'address' in request.data:
        order.address = Address.objects.get(id=request.data['address'])

    order.save()
    return Response(status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove(request):
    order_product = OrderProduct.objects.get(id=request.data['id'])
    order = order_product.order

    order_product.delete()
    order.price = order.price - order_product.price
    order.save()

    if OrderProduct.objects.filter(order=order).count() == 0:
        order.delete()
    return Response(status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_orders(request):
    user = CustomUser.objects.get(id=request.user.id)
    if user.is_vendor:
        vendor = Vendor.objects.get(user=user)
        orders = Order.objects.filter(vendor=vendor)
    else:
        orders = Order.objects.filter(user=user)

    return Response(OrderSerializer(orders, many=True).data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_comment(request):
    order = Order.objects.get(id=request.data['order'])
    user = CustomUser.objects.get(id=request.user.id)
    serializer = AddCommentSerializer(data=request.data,
                                      context={'order': order,
                                               'user': user})
    if serializer.is_valid():
        serializer.save()
        return Response(status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_comments(request):
    user = CustomUser.objects.get(id=request.user.id)
    if user.is_vendor:
        vendor = Vendor.objects.get(user=user)
    else:
        vendor = Vendor.objects.get(id=request.query_params.get('vendor'))

    orders = Order.objects.filter(vendor=vendor)

    return Response(OrderSerializer(orders, many=True).data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def reply_comment(request):
    cm = Comment.objects.get(id=request.data['comment'])

    cm.reply = request.data['reply']
    cm.save()
    return Response(status=status.HTTP_200_OK)


