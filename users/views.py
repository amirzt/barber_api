from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from users.models import CustomUser, Country, City, ServiceLine, Vendor, Customer, Address
from users.serializers import RegistrationSerializer, AddVendorSerializer, CountrySerializer, CitySerializer, \
    ServiceLineSerializer, VendorSerializer, CustomerSerializer, AddAddressSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    try:
        user = CustomUser.objects.get(phone=request.data['phone'])

        if user.check_password(request.POST.get('password')):
            user.is_active = True
            user.save()

            token, created = Token.objects.get_or_create(user=user)

            return Response({
                'token': token.key,
                'exist': True
            }, status=200)
        else:
            return Response({
                'message': 'Password is incorrect'
            }, status=403)

    except CustomUser.DoesNotExist:
        user_serializer = RegistrationSerializer(data=request.data)

        if user_serializer.is_valid():
            user = user_serializer.save()

            user.is_active = True
            user.save()

            token, created = Token.objects.get_or_create(user=user)

            return Response({
                'token': token.key,
                'exist': False
            })

        else:
            return Response(user_serializer.errors, status=400)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def register_vendor(request):
    user = request.user
    try:
        vendor = Vendor.objects.get(user=user)
        return Response({"message": "Vendor already exist"}, status=status.HTTP_403_FORBIDDEN)
    except Vendor.DoesNotExist:
        serializer = AddVendorSerializer(data=request.data,
                                         context={"user": user})

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([AllowAny])
def countries(request):
    country_list = Country.objects.all()
    return Response(CountrySerializer(country_list, many=True).data)


@api_view(['GET'])
@permission_classes([AllowAny])
def cities(request):
    city_list = City.objects.all()
    if 'country' in request.query_params:
        city_list = city_list.filter(country_id=request.query_params.get('country'))
    return Response(CitySerializer(city_list, many=True).data)


@api_view(['GET'])
@permission_classes([AllowAny])
def service_lines(request):
    service_line_list = ServiceLine.objects.all()
    return Response(ServiceLineSerializer(service_line_list, many=True).data)

@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def profile(request):
    user = CustomUser.objects.get(id=request.user.id)

    if request.method == 'GET':
        if user.is_vendor:
            vendor = Vendor.objects.get(user=user)
            return Response(VendorSerializer(vendor).data)
        else:
            customer = Customer.objects.get(user=user)
            return Response(CustomerSerializer(customer).data)
    elif request.method == 'PUT':
        if user.is_vendor:
            vendor = Vendor.objects.get(user=user)
            if 'name' in request.data:
                vendor.name = request.data['name']
            if 'vendor_image' in request.data:
                vendor.image = request.data['vendor_image']
            if 'service_line' in request.data:
                vendor.service_line = ServiceLine.objects.get(id=request.data['service_line'])
            if 'is_active' in request.data:
                vendor.is_active = request.data['is_active']
            if 'start_hour' in request.data:
                vendor.start_hour = request.data['start_hour']
            if 'end_hour' in request.data:
                vendor.end_hour = request.data['end_hour']
            vendor.save()
            return Response(status=status.HTTP_200_OK)
        else:
            pass


@api_view(['POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def address(request):
    if request.method == 'POST':
        user = CustomUser.objects.get(id=request.user.id)
        if user.is_vendor:
            addresses = Address.objects.filter(user=user)
            if addresses.count() != 0:
                addresses.delete()

        serializer = AddAddressSerializer(data=request.data,
                                          context={'user': user})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        ad = Address.objects.get(id=request.data['id'])
        ad.delete()
        return Response(status=status.HTTP_200_OK)
