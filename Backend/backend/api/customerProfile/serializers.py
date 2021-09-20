from rest_framework import serializers

from user_profile.models import Customer,Farmer

from django.contrib.auth import get_user_model


User = get_user_model()


class CustomerSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    
    class Meta:
        model = Customer
        fields = [ 'url','avatar','id', 'user',
                  'full_name','address','city','state',]


class FarmerSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    
    class Meta:
        model = Farmer
        fields = [ 'url','avatar','id', 'user',
                  'full_name','address','city','state','company_name',]



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'full_name', 'email', 'username']