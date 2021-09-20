from django.shortcuts import get_object_or_404
from rest_framework import authentication, permissions,filters
from rest_framework.permissions import AllowAny, IsAdminUser,IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.viewsets import generics
from rest_framework import status

from user_profile.models import Farmer,Land
from .serializers import LandSerializer



class LandAdd(generics.CreateAPIView):
    serializer_class = LandSerializer
    permission_classes=[AllowAny]

    def perform_create(self, serializer):
        username=self.request.GET.get('user__username')
        farmer=Farmer.objects.filter(user__username=username)
        serializer.save(user=farmer.first())

#     def post(self,request):
#         serializer = LandSerializer(data=request.data)
#         username=self.request.GET.get('user__username')
#         farmer=Farmer.objects.filter(user__username=username)

#         if serializer.is_valid():
#             serializer.save(user=farmer.first())
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class LandAdd(ModelViewSet):

#     serializer_class = LandSerializer
#     lookup_field='id'

#     permission_classes=[AllowAny]
#     def perform_create(self, serializer):
#         username=self.request.GET.get('user__username')
#         farmer=Farmer.objects.filter(user__username=username)
#         serializer.save(user=farmer.first())



class LandView(ModelViewSet): 
    serializer_class = LandSerializer
    lookup_field='id'

    permission_classes=[AllowAny]

    
    def get_queryset(self):
        username = self.request.GET.get('user__username')
        return Land.objects.filter(user__user__username=username)