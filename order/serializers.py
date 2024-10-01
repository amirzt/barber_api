from rest_framework import serializers

from order.models import Order, OrderProduct, Comment, Transaction
from product.models import Product
from product.serializers import ProductSerializer, ProductCustomizationSerializer
from users.models import Wallet
from users.serializers import UserSerializer, AddressSerializer, VendorSerializer


class OrderProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    customization = ProductCustomizationSerializer()

    class Meta:
        model = OrderProduct
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    address = AddressSerializer()
    products = serializers.SerializerMethodField('get_products')
    vendor = VendorSerializer()
    comments = serializers.SerializerMethodField('get_comments')
    transaction = serializers.SerializerMethodField('get_transaction')

    @staticmethod
    def get_products(obj):
        products = OrderProduct.objects.filter(order=obj)
        return OrderProductSerializer(products, many=True).data

    @staticmethod
    def get_comments(obj):
        comments = Comment.objects.filter(order=obj)
        return CommentSerializer(comments, many=True).data

    @staticmethod
    def get_transaction(obj):
        transaction = Transaction.objects.filter(order=obj)
        return TransactionSerializer(transaction, many=True).data

    class Meta:
        model = Order
        fields = '__all__'


class AddOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['vendor', ]

    def save(self, **kwargs):
        order = Order(vendor=self.context.get('vendor'),
                      user=self.context.get('user'))
        order.save()
        return order


class AddOrderProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderProduct
        fields = ['product', 'customization', 'quantity']

    def save(self, **kwargs):
        order_product = OrderProduct(order=self.context.get('order'),
                                     product=self.validated_data['product'],
                                     customization=self.validated_data['customization'],
                                     quantity=self.validated_data['quantity'],
                                     price=(self.validated_data['customization'].price
                                            + (self.validated_data['product'].price *
                                               ((100 -Product.objects.get(id=self.validated_data['product'].id).discount) / 100)))
                                           * self.validated_data['quantity']
                                     )
        order_product.save()
        return order_product


class AddCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['order', 'content', 'rating']

    def save(self, **kwargs):
        comment = Comment(order=self.validated_data['order'],
                          content=self.validated_data['content'],
                          rating=self.validated_data['rating'],
                          user=self.context.get('user'),
                          vendor=self.context.get('vendor'))
        comment.save()
        return comment


class AddTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['order', 'payment_status', 'tracking_code']

    def save(self, **kwargs):
        transaction = Transaction(order=self.validated_data['order'],
                                  payment_status=self.validated_data['payment_status'],
                                  tracking_code=self.validated_data['tracking_code'])
        transaction.save()

        # save wallet balance
        if self.validated_data['payment_status'] == 'success':
            wallet = Wallet.objects.get(user=self.validated_data['order'].vendor.user)
            wallet.balance += self.validated_data['order'].price
            wallet.save()
        return transaction