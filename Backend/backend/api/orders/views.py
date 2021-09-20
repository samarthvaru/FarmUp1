


import json


from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from user_profile.models import Customer
from cart.models import Cart
from products.models import Product
from rest_framework import viewsets
from rest_framework import generics 
from orders.models import Order,SoldOrderItems
from .serializers import DetailedOrderSerializer,OrderSerializer,SoldOrderItemsSerializer
from billing.models import BillingProfile
from rest_framework import viewsets
from rest_framework import status


class OrderView(generics.ListAPIView): 
    # define queryset 
    permission_classes = [AllowAny]
    queryset = Order.objects.all() 
      
    # specify serializer to be used 
    serializer_class = OrderSerializer

class CustomerOrderView(generics.ListAPIView): 


    def get(self, request, *args, **kwargs):
        username=request.GET.get("user__username")
        profiles = Customer.objects.filter(user__username=username)

        if not profiles.count() == 1:
            return Response({'error': 'Profile Doesn\'t exist'}, status=400)

        order_obj = Order.objects.get_order(profiles.first())

        return Response({'orders':OrderSerializer(order_obj,context={'request':request}).data,})
    



class CheckoutView(APIView):
    permission_classes = [AllowAny]   ##IsAuthenticated

    def get(self, request, *args, **kwargs):

        # profile_id = request.GET.get("profile_id")
        username=request.GET.get("user__username")

        # if profile_id == None:
        #     return Response({'error': 'Profile Id Not Found'}, status=400)
        # users = User.objects.filter( customer_set__user =  )
        # user_avatar = Avatar.objects.filter( user__in = users )

        profiles = Customer.objects.filter(user__username=username)

        if not profiles.count() == 1:
            return Response({'error': 'Profile Doesn\'t exist'}, status=400)

        cart_obj, _ = Cart.objects.get_existing_or_new(request,username)

        if cart_obj.total_cart_products == 0:
            return Response({'error': 'Cart Is Empty'}, status=400)
        


        order_obj = Order.objects.get_order(profiles.first())

        cart_obj.used=True
        cart_obj.save()

        return Response({
            "order": DetailedOrderSerializer(order_obj, context={'request': request}).data,
            
        })

    def post(self, request, *args, **kwargs):
        username=request.GET.get("user__username")

        if username == None:
            return Response({'error': 'Profile Id Not Found'}, status=400)

        profiles = Customer.objects.filter(user__username=username)

        if not profiles.count() == 1:
            return Response({'error': 'Profile Doesn\'t exist'}, status=400)

        order_obj = Order.objects.get_order(profiles.first())

        return Response(DetailedOrderSerializer(order_obj,context={'request': request}).data)



    
class SoldOrderItemsView(viewsets.ModelViewSet):
    serializer_class = SoldOrderItemsSerializer
    lookup_field='id'
    permission_classes=[AllowAny]

    def get_queryset(self):
        username = self.request.GET.get('user__username')
        return SoldOrderItems.objects.filter(sold_by=username).order_by('-timestamp')
    
    def put(self, request, id):
        data_in = request.data
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=False)
        serializer.is_valid(raise_exception=True)

        if instance is None:
            lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
            lookup_value = self.kwargs[lookup_url_kwarg]
            extra_kwargs = {self.lookup_field: lookup_value}
            serializer.save(**extra_kwargs)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        serializer.save()
        data_out = serializer.data
        print(serializer.data)
        return Response(serializer.data)
    
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


    
    




