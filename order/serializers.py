from rest_framework import serializers

from order.models import Order, OrderProduct, Comment, Transaction
from product.serializers import ProductSerializer, ProductCustomizationSerializer
from users.serializers import UserSerializer, AddressSerializer, VendorSerializer


class OrderProductSerializer(serializers.Serializer):
    product = ProductSerializer()
    customization = ProductCustomizationSerializer()

    class Meta:
        model = OrderProduct
        fields = '__all__'


class CommentSerializer(serializers.Serializer):
    class Meta:
        model = Comment
        fields = '__all__'


class TransactionSerializer(serializers.Serializer):
    class Meta:
        model = Transaction
        fields = '__all__'


class OrderSerializer(serializers.Serializer):
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


class AddOrderSerializer(serializers.Serializer):
    class Meta:
        model = Order
        fields = ['vendor', ]

    def save(self, **kwargs):
        order = Order(vendor=self.validated_data['vendor'],
                      user=self.context.get('user'))
        order.save()
        return order


class AddOrderProductSerializer(serializers.Serializer):
    class Meta:
        model = OrderProduct
        fields = ['product', 'customization', 'quantity']

    def save(self, **kwargs):
        order_product = OrderProduct(order=self.context.get('order'),
                                     product=self.validated_data['product'],
                                     customization=self.validated_data['customization'],
                                     quantity=self.validated_data['quantity'],
                                     price=self.validated_data['customization'].price
                                           + self.validated_data['product'].price)
        order_product.save()
        return order_product


class AddCommentSerializer(serializers.Serializer):
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