from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from users.models import CustomUser, Country, City, ServiceLine
from users.serializers import RegistrationSerializer, AddVendorSerializer, CountrySerializer, CitySerializer, \
    ServiceLineSerializer


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
    serializer = AddVendorSerializer(data=request.data)

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
    return Response(CitySerializer(city_list, many=True).data)


@api_view(['GET'])
@permission_classes([AllowAny])
def service_lines(request):
    service_line_list = ServiceLine.objects.all()
    return Response(ServiceLineSerializer(service_line_list, many=True).data)
