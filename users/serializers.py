from rest_framework import serializers

from users.models import CustomUser, Address, Country, City, Vendor, ServiceLine, Customer, Wallet


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['password', 'phone', 'is_vendor']
        extra_kwargs = {"password": {"write_only": True}}

    def save(self, **kwargs):
        user = CustomUser(phone=self.validated_data['phone'],
                          is_vendor=self.validated_data['is_vendor'])
        user.set_password(self.validated_data['password'])
        user.save()

        wallet = Wallet(user=user)
        wallet.save()

        if not user.is_vendor:
            customer = Customer(user=user)
            customer.save()
        return user


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'


class CitySerializer(serializers.ModelSerializer):
    country = CountrySerializer()
    class Meta:
        model = City
        fields = '__all__'


class AddressSerializer(serializers.ModelSerializer):
    city = CitySerializer()

    class Meta:
        model = Address
        fields = '__all__'


class AddAddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = Address
        fields = ['city', 'title', 'address', 'latitude', 'longitude', 'postal_code']

    def save(self, **kwargs):
        address = Address(user=self.context.get('user'),
                          city=self.validated_data['city'],
                          title=self.validated_data['title'],
                          address=self.validated_data['address'],
                          latitude=self.validated_data['latitude'],
                          longitude=self.validated_data['longitude'],
                          postal_code=self.validated_data['postal_code'])
        address.save()
        return address


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    address = serializers.SerializerMethodField('get_address')
    wallet = serializers.SerializerMethodField('get_wallet')

    @staticmethod
    def get_address(obj):
        addresses = Address.objects.filter(user=obj)
        return AddressSerializer(addresses, many=True).data


    @staticmethod
    def get_wallet(obj):
        wallet = Wallet.objects.get(user=obj)
        return WalletSerializer(wallet).data

    class Meta:
        model = CustomUser
        fields = ['phone', 'name', 'image', 'is_vendor', 'address', 'wallet']


class ServiceLineSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceLine
        fields = '__all__'


class VendorSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    service_line = ServiceLineSerializer()

    class Meta:
        model = Vendor
        fields = '__all__'


class AddVendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ['name', 'image']

    def save(self, **kwargs):
        vendor = Vendor(user=self.context.get('user'),
                        name=self.validated_data['name'],
                        image=self.validated_data['image'])
        vendor.save()
        return vendor

class CustomerSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Customer
        fields = '__all__'


class AddCustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['user']

    def save(self, **kwargs):
        customer = Customer(user=self.validated_data['user'])
        if kwargs.get('image'):
            customer.image = kwargs.get('image')
        customer.save()
        return customer
