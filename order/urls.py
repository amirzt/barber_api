from rest_framework.urls import path
from order import views

urlpatterns = [
    path('create_order/', views.create_order, name='create_order'),
    path('update_order/', views.update_order, name='update_order'),

    path('get_orders/', views.get_orders, name='get_orders'),
    path('remove/', views.remove, name='remove'),
    path('add_comment/', views.add_comment, name='add_comment'),
    path('get_comments/', views.get_comments, name='get_comments'),

    path('reply_comment/', views.reply_comment, name='reply_comment'),

    path('get_transactions/', views.get_transactions, name='get_transactions'),
    path('pay/', views.pay, name='pay'),
]