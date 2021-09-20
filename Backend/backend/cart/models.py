from django.contrib.auth import get_user_model
from django.db import models

from products.models import Product
from user_profile.models import Customer
from core.settings import AUTH_USER_MODEL
User = get_user_model()


class CartManager(models.Manager):
    def get_existing_or_new(self, request,user_username):
        created = False
        cart_id = request.session.get('cart_id')
        # if self.get_queryset().filter(id=cart_id, used=False).count() == 1:
        #     obj = self.model.objects.get(id=cart_id)
        if self.get_queryset().filter(user__username=user_username, used=False).count() == 1:
            obj = self.model.objects.get(user__username=user_username, used=False)
            request.session['cart_id'] = obj.id
        else:
            user=User.objects.get(username=user_username)
            obj = self.model.objects.create(user=user)
            request.session['cart_id'] = obj.id
            created = True
        return obj, created


class Cart(models.Model):
    user = models.ForeignKey(
        AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE)
    used = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = CartManager()

    def __str__(self):
        return str(self.id)

    @property
    def total(self):
        total = 0
        for item in self.products.all():
            total += int(item.quantity) * float(item.product.price)
        return total

    @property
    def tax_total(self):
        total = 0
        for item in self.products.all():
            total += int(item.quantity) * float(item.product.price) * \
                float(item.product.tax) / 100
        return total

    @property
    def total_cart_products(self):
        return sum(item.quantity for item in self.products.all())


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE, related_name="products")

    def __str__(self):
        return str(self.product)+' '+str(self.id)

    class Meta:
        unique_together = (
            ('product', 'cart')
        )
        


    
