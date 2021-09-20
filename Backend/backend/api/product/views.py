from django.shortcuts import get_object_or_404
from rest_framework import authentication, permissions,filters
from rest_framework.permissions import AllowAny, IsAdminUser,IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.viewsets import generics

from products.models import Product
from user_profile.models import Farmer
from .serializers import ProductSerializer
from rest_framework.parsers import MultiPartParser,FormParser

class ProductViewSet(ModelViewSet):
    serializer_class = ProductSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        max_price = self.request.GET.get('max_price')
        min_price = self.request.GET.get('min_price')
        sort = self.request.GET.get('sort')
        keyword = self.request.GET.get('keyword')
        return Product.objects.filter_products(keyword, sort, min_price, max_price).order_by('-timestamp')

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'list' or self.action == 'retrieve':
            permission_classes = [AllowAny]
        else:
            permission_classes = [AllowAny] #IsAuthenticated
        return [permission() for permission in permission_classes]


class RelatedProductView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, id, *args, **kwargs):
        product_id=request.data.get('id')
        print(product_id)
        if not product_id:
            return Response({"error": "Product Id Not Found"}, status=400)
        product = get_object_or_404(Product, id=product_id)
        products_serialized = ProductSerializer(
            product.get_related_products(), many=True, context={'request': request})
        return Response(products_serialized.data)

    @classmethod
    def get_extra_actions(cls):
        return []

class ProductAdd(generics.CreateAPIView):
    serializer_class = ProductSerializer
    lookup_field = 'slug'
    parser_classes=[MultiPartParser,FormParser]

    def perform_create(self, serializer):
        username=self.request.GET.get('user__username')
        farmer=Farmer.objects.filter(user__username=username)
        serializer.save(sold_by=farmer.first())



class FarmerProductViewSet(ModelViewSet):
    serializer_class = ProductSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        username = self.request.GET.get('user__username')
        return Product.objects.filter(sold_by__user__username=username)


class ProductListDetailfilter(generics.ListAPIView):

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter]
    # '^' Starts-with search.
    # '=' Exact matches.
    search_fields = ['^slug']
