
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from user_profile.models import Customer
from orders.models import Order
from rest_framework import status
from api.orders.serializers import DetailedOrderSerializer, OrderSerializer


class UserOrderList(APIView):
    permission_classes = [AllowAny]  ##IsAuthenticated

    def get(self, request, *args, **kwargs):
        username=request.GET.get('user__username')
        profiles = Customer.objects.filter(user__username=username)
        orders = Order.objects.filter(customer=profiles.first()).all().order_by('-timestamp')
        return Response(OrderSerializer(orders, many=True).data)


class OrderDetail(APIView):
    permission_classes = [AllowAny]  ##IsAuthenticated
   
    def get(self, request, *args, order_id, **kwargs):
        order_obj: Order = get_object_or_404(Order, order_id=order_id)
        serializer_context = {
            'request': request,
        }
        # if order_obj.customer.user != username:
        #     return Response(status=401)
        
        return Response(DetailedOrderSerializer(order_obj,context={'request': request}).data)

    def put(self,request,*args,order_id,**kwargs):
        address=request.data.get('address')
        city=request.data.get('city')
        state=request.data.get('state')
        order_obj: Order = get_object_or_404(Order,order_id=order_id)
        if(address):
            order_obj.address=address
        if(city):
            order_obj.city=city
        if(state):
            order_obj.state=state
        order_obj.save()
        serializer_context = {
            'request' : request
        }

        return Response(DetailedOrderSerializer(order_obj,context={'request':request}).data)

    def delete(self, request, *args,order_id, **kwargs):
        instance = get_object_or_404(Order,order_id=order_id)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)