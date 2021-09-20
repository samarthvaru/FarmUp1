from rest_framework import serializers
from api.customerProfile.serializers import FarmerSerializer

from products.models import Product,Tag
from api.customerProfile.serializers import FarmerSerializer


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['title', 'slug']


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    tag_list = TagSerializer(many=True, read_only=True)
    sold_by= FarmerSerializer(read_only=True)


    class Meta:
        model = Product
        fields = ['id', 'image', 'title', 'slug',
                  'featured', 'description', 'original_price', 'price', 'tag_list','sold_by','timestamp']
        ordering=['timestamp']
# class ProductListSerializer(serializers.ModelSerializer):


#     class Meta:
#         model = Product
#         fields = [ 'name', 'description',
#                   'sold_by']


# class ProductDetailSerializer(serializers.ModelSerializer):


#     class Meta:
#         model = Product
#         fields = ['name', 'description', 'price',
#                   'sold_by', 'date',]