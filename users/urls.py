from rest_framework.urls import path

from users import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('register_vendor/', views.register_vendor, name='register_vendor'),
    path('countries/', views.countries, name='countries'),
    path('cities/', views.cities, name='cities'),
    path('service_lines/', views.service_lines, name='service_lines'),
    path('profile/', views.profile, name='profile'),
    path('address/', views.address, name='address'),
    path('change_admin_password/', views.change_admin_password, name='change_admin_password'),
    path('splash/', views.splash, name='product_customization'),

]