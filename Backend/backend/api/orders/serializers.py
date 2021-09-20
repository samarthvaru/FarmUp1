# from rest_framework import serializers

# from orders.models import Order,OrderItem
# from api.customerProfile.serializers import CustomerSerializer
# from api.product.serializers import ProductSerializer

# class OrderItemSerializer(serializers.HyperlinkedModelSerializer):

#     class Meta:
#         model = OrderItem
#         fields = [ 'url','id', 'product','quantity']


# class OrderSerializer(serializers.HyperlinkedModelSerializer):
#     order_items=OrderItemSerializer(read_only=True,many=True)

    
#     class Meta:
#         model = Order
#         fields = [ 'url','id', 'customer','status','created_at','order_items']

from rest_framework import serializers
from rest_framework.fields import IntegerField

from api.customerProfile.serializers import CustomerSerializer
from cart.serializers import CartSerializer
from api.product.serializers import ProductSerializer
from orders.models import Order,SoldOrderItems


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = [
            'order_id',
            'status',
            'timestamp',
            'shipping_total',
            'cart_total',
            'tax_total',
            'total'
        ]


class DetailedOrderSerializer(serializers.ModelSerializer):
    customer=CustomerSerializer()
    cart = CartSerializer()

    class Meta:
        model = Order
        fields = [
            'customer',
            'order_id',
            'cart',
            'status',
            'timestamp',
            'shipping_total',
            'cart_total',
            'tax_total',
            'total',
            'total_in_paise',
            'address',
            'city',
            'state'
        ]

        total_in_paise = IntegerField(source='total_in_paise')


class SoldOrderItemsSerializer(serializers.ModelSerializer):

    class Meta:
        model = SoldOrderItems
        fields = [
            'id',
            'item',
            'sold_by',
            'quantity',
            'order_id',
            'status',
            'timestamp',
            'address',
            'state',
            'city'
        ]



