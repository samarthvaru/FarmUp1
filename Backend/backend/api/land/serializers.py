from rest_framework import serializers

from user_profile.models import Land
from api.customerProfile.serializers import FarmerSerializer



class LandSerializer(serializers.HyperlinkedModelSerializer):
    user= FarmerSerializer(read_only=True)


    class Meta:
        model = Land
        fields = ['id', 'user', 'city', 'latitude',
                  'longitude',]