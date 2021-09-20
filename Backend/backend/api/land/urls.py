from . import views
from django.urls import path,include
from .views import *


  

urlpatterns = [
    path("", LandView.as_view({'get':'list',})),
    path("<id>/", LandView.as_view({'get':'retrieve'})),
    path("add/addLand/",LandAdd.as_view()),
    path("<id>/partialupdate/", LandView.as_view({'put': 'update'})),
    path("<id>/delete/", LandView.as_view({'delete': 'destroy'})),

    

] 