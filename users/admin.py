from django.contrib import admin

from users.models import CustomUser, Vendor, Customer, Address, Country, City, ServiceLine, Wallet, VendorServiceLine


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('phone', 'date_joint')
    search_fields = ('phone', 'name')
    fields = (
        'phone', 'name', 'is_vendor', 'is_visible', 'is_active', 'is_staff', 'app_type', 'version')


@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'created_at', 'updated_at')
    search_fields = ('name', 'user__name', 'user__phone')
    fields = ('name', 'user', 'image')


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user', 'image', 'created_at', 'updated_at')
    search_fields = ('user__name', 'user__phone')
    fields = ('user', 'image')


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('title', 'address', 'user', 'created_at', 'updated_at')
    search_fields = ('title', 'address', 'user__name', 'user__phone')
    fields = ('user', 'title', 'address', 'latitude', 'longitude', 'city', 'postal_code')


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    fields = ('name',)

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'country')
    search_fields = ('name', 'country__name')
    fields = ('name', 'country')


@admin.register(ServiceLine)
class ServiceLineAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    fields = ('name', 'image')


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ('user', 'balance', 'updated_at')
    search_fields = ('user__name', 'user__phone')
    fields = ('user', 'balance')

admin.site.register(VendorServiceLine)


