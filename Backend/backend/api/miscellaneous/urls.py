from . import views
from django.urls import path,include



urlpatterns = [
    path("soldItems/", views.YourView.as_view()),
    path("statusCount/",views.StatusCountView.as_view())
]