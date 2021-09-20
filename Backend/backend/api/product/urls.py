from django.urls import path,include
from .views import *
from rest_framework import routers 

# router = routers.DefaultRouter() 
  
# # define the router path and viewset to be used 
# router.register('Products', ProductView) 
  
# # specify URL Path for rest_framework 
# urlpatterns = [ 
#     path('', include(router.urls)), 

# ]


urlpatterns = [
    path("list/", ProductViewSet.as_view({'get': 'list'})),
    path("own/list/", FarmerProductViewSet.as_view({'get': 'list'})),
    path("own/list/<slug>/", FarmerProductViewSet.as_view({'get': 'retrieve'})),
    path("list/<slug>/", ProductViewSet.as_view({'get': 'retrieve'})),
    path("own/list/<slug>/partialupdate/", FarmerProductViewSet.as_view({'put': 'update'})),
    path("own/list/<slug>/delete/", FarmerProductViewSet.as_view({'delete': 'destroy'})),
    path("related/<id>/", RelatedProductView.as_view()),
    path("addProduct/",ProductAdd.as_view()),
    path('search/', ProductListDetailfilter.as_view(), name='searchproduct'),
    # path("updateProduct/",ProductView.as_view()),
]