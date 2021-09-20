from . import views
from django.urls import path,include
from .views import *


  

urlpatterns = [
    path("", OrderView.as_view()),
    path("cust/",CustomerOrderView.as_view()),
    path("checkout/",CheckoutView.as_view()),
    path('soldItems/',SoldOrderItemsView.as_view({'get':'list'})),
    path('soldItems/<id>/',SoldOrderItemsView.as_view({'get':'retrieve'})),
    path("soldItems/<id>/", SoldOrderItemsView.as_view({'put': 'put'})),
    path('soldItems/<id>/', SoldOrderItemsView.as_view({'delete': 'destroy'}))
    

] 