from datetime import datetime
from orders.models import SoldOrderItems
from rest_framework import views
from rest_framework.response import Response

from .serializers import SelleroftheMonthSerializer,OrderStatusCountSerializer
from rest_framework.permissions import AllowAny

from django.db.models import Count 


class YourView(views.APIView):
    permission_classes=[AllowAny]

    def get(self, request):
        current_month = datetime.now().month  
        v=SoldOrderItems.objects.values('sold_by').filter(timestamp__month=current_month).annotate(total=Count('id')) 
        yourdata=v.latest('total')
        results = SelleroftheMonthSerializer(yourdata).data
        return Response(results)

class StatusCountView(views.APIView):
    permission_classes=[AllowAny]

    def get(self,request):
        username=request.GET.get('user__username')
        pending=SoldOrderItems.objects.filter(sold_by=username).filter(status='PENDING').count()
        delivered=SoldOrderItems.objects.filter(sold_by=username).filter(status='DELIVERED').count()
        
        context={'pending':pending,'delivered':delivered}
        results=OrderStatusCountSerializer(context).data
        return Response(results)




