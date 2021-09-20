from . import views
from django.urls import path,include
from .views import *
from rest_framework import routers 

# urlpatterns = [
#     path('customers/', views.customer_list.as_view()),
#     path('customers/<pk>', views.customer_detail.as_view(),name="customer-detail-view"),
# ]
router = routers.DefaultRouter() 

  
# define the router path and viewset to be used 
router.register('Farmers', farmerView) 
  



  
# define the router path and viewset to be used 
router.register('Customers', customerView) 
  
# specify URL Path for rest_framework 
urlpatterns = [ 
    path('', include(router.urls)),
    path('farm/myProfile/',FarmerProfile.as_view({'get': 'list'})),
    path('cust/myProfile/',CustomerProfile.as_view({'get': 'list'}))



] 