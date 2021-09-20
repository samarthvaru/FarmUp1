from django.contrib import admin

from .models import Farmer, Customer, User,Land

# Register your models here.
class FarmerProfileAdmin(admin.ModelAdmin):
    list_display = ['username', 'full_name']

class UserProfileAdmin(admin.ModelAdmin):

    list_display = ['username', 'id','email']

admin.site.register(Farmer, FarmerProfileAdmin)
admin.site.register(User,UserProfileAdmin)
admin.site.register(Customer,FarmerProfileAdmin)

class LandAdmin(admin.ModelAdmin):
    list_display = ['username','name']

admin.site.register(Land,LandAdmin)