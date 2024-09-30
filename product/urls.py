from rest_framework.urls import path

from product import views

urlpatterns = [
    path('get_product/', views.get_product, name='products'),
    path('add_product/', views.add_product, name='add_product'),
    path('update_product/', views.update_product, name='update_product'),

    path('product_image/', views.product_image, name='product_image'),

    path('customization/', views.customization, name='product_customization'),
]