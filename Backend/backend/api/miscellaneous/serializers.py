from rest_framework import serializers

class SelleroftheMonthSerializer(serializers.Serializer):
   """Your data serializer, define your fields here."""
   sold_by = serializers.CharField(max_length=255)
   total = serializers.IntegerField()

class OrderStatusCountSerializer(serializers.Serializer):
   """Your data serializer, define your fields here."""
   pending=serializers.IntegerField()
   delivered= serializers.IntegerField()