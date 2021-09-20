from rest_framework import serializers
from rest_framework.fields import Field

from api.product.serializers import ProductSerializer
from api.customerProfile.serializers import CustomerSerializer

from .models import Cart, CartItem


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity']


class CartSerializer(serializers.ModelSerializer):
    products = CartItemSerializer(read_only=True, many=True)


    class Meta:
        model = Cart
        total = Field(source='total')
        total_cart_products = Field(source='total_cart_products')
        fields = ['id', 'user', 'products', 'total', 'total_cart_products']