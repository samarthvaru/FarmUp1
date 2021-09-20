


from django.contrib import admin

from .models import Order,SoldOrderItems



@admin.register(SoldOrderItems)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('__str__','item','timestamp',)

@admin.register(Order)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('order_id','cart','timestamp',)



