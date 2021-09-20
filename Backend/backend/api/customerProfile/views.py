from rest_framework import generics 
from .serializers import CustomerSerializer,FarmerSerializer
from user_profile.models import Customer,Farmer
from rest_framework import viewsets
from rest_framework import authentication, permissions

from rest_framework import renderers,filters
from rest_framework.response import Response



# class customer_list(generics.ListAPIView):
#     queryset = Customer.objects.all()
#     serializer_class = CustomerSerializer

# class customer_detail(generics.RetrieveUpdateDestroyAPIView):
#     queryset =Customer.objects.all()
#     serializer_class = CustomerSerializer

# create a viewset 
class customerView(viewsets.ModelViewSet): 
    # define queryset 
    permission_classes = [permissions.AllowAny]
    queryset = Customer.objects.all() 
      
    # specify serializer to be used 
    serializer_class = CustomerSerializer

class farmerView(viewsets.ModelViewSet): 
    permission_classes = [permissions.AllowAny]
    # define queryset 
    queryset = Farmer.objects.all() 
    # specify serializer to be used 
    serializer_class = FarmerSerializer

class FarmerProfile(viewsets.ModelViewSet):
    serializer_class = FarmerSerializer

    def get_queryset(self):
        username = self.request.GET.get('user__username')
        return Farmer.objects.filter(user__username=username)

class CustomerProfile(viewsets.ModelViewSet):
    serializer_class = CustomerSerializer

    def get_queryset(self):
        username = self.request.GET.get('user__username')
        return Customer.objects.filter(user__username=username)




