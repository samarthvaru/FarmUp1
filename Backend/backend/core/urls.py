"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)
from .views import BlacklistTokenUpdateView
from django.conf import settings
from django.conf.urls.static import static





urlpatterns = [
    path('admin/', admin.site.urls),
    path('token/',TokenObtainPairView.as_view(),name="token_obtain_pair"),
    path('token/refresh/',TokenRefreshView.as_view(),name="token_refresh"),
    path('register/', include('api.registration.urls')),
    path('accounts/', include('accounts.urls')),
    path('posts/', include('api.post.urls')),
    path('products/', include('api.product.urls')),
    path('users/',include('api.customerProfile.urls')),
    path('cart/', include('cart.urls')),
    path('comments/', include('api.comment.urls')),
    path('orders/',include('api.orders.urls')),
    path('miscellaneous/',include('api.miscellaneous.urls')),
    path('land/',include('api.land.urls')),
    path('profiles/', include('billing.urls')),
    path('logout/blacklist/', BlacklistTokenUpdateView.as_view(),
         name='blacklist')

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)


admin.site.site_header = 'Farm Up admin Panel'
admin.site.site_title = 'Farm Up'