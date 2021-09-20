
from django.utils import timezone
from django.db import models
from django.db.models.signals import post_save, pre_save,post_delete

from user_profile.models import Customer
from cart.models import Cart
from core.utils import unique_product_id_generator
from products.models import Product

STATUS_CHOICES = (
    ('created', 'Created'),
    ('paid', 'Paid'),
    ('shipped', 'Shipped'),
    ('delivered', 'Delivered'),
    ('refunded', 'Refunded'),
)


class OrderManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter()

    def get_order(self, customer_id: Customer):
        qs = self.get_queryset().filter(
            customer_id__user=customer_id.user,cart__used=False)
        if qs.count() == 0:
            cart = customer_id.user.cart_set.filter(used=False).first()
            order = Order(customer=customer_id, cart=cart)
            order.save()
            return order
        else:
            order = qs.first()
            order.customer = customer_id
            order.save()
            return order


class Order(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, null=True, blank=True)
    order_id = models.CharField(max_length=120, blank=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    status = models.CharField(choices=STATUS_CHOICES,
                              default='created', max_length=120)
    timestamp = models.DateTimeField(auto_now_add=True)
    shipping_total = models.DecimalField(
        default=70, max_digits=10, decimal_places=2)
    address=models.TextField(blank=True,null=True,default="")
    city=models.CharField(max_length=20,blank=True,null=True,default="")
    state=models.CharField(max_length=20,blank=True,null=True,default="")
    
    

    objects = OrderManager()

    def __str__(self):
        return self.order_id

    @property
    def total_in_paise(self):
        return int(self.total * 100)

    def check_done(self):
        customer = self.customer
        total = self.total
        cart = self.cart
        active = self.active
        if active and total > 0 and cart and customer:
            return True
        return False

    def mark_paid(self):
        if self.check_done():
            self.cart.used = True
            self.cart.save()
            self.status = 'paid'
            self.save()
            return True
        return False

    @property
    def cart_total(self):
        return self.cart.total

    @property
    def tax_total(self):
        return self.cart.tax_total

    @property
    def total(self):
        return float(self.cart_total) + float(self.tax_total) + float(self.shipping_total)


def pre_save_create_order_id(sender, instance, *args, **kwargs):
    if not instance.order_id:
        instance.order_id = unique_product_id_generator(instance)


pre_save.connect(pre_save_create_order_id, sender=Order)





class SoldOrderItems(models.Model):

    CHOICES=((
    ('PENDING', 'PENDING'),
    ('DELIVERED', 'DELIVERED'),
    ))

    item=models.CharField(max_length=255)
    quantity=models.IntegerField(default=1)
    timestamp = models.DateTimeField(auto_now_add=True)
    order_id=models.CharField(blank=True, null=True,max_length=255)
    status=models.CharField(choices=CHOICES,default='PENDING',max_length=255)
    address=models.TextField(blank=True,null=True,default="")
    city=models.CharField(max_length=20,blank=True,null=True,default="")
    state=models.CharField(max_length=20,blank=True,null=True,default="")
    sold_by=models.CharField(max_length=255,blank=True, null=True)

    def __str__(self):
        return str(self.id)



def post_save_create_soldorder(sender,instance,*args,**kwargs):
    timestamp=instance.timestamp
    # order_id=instance.order_id
    cart=instance.cart

    for item in cart.products.all():
        if item.product:
            query_set=SoldOrderItems.objects.filter(item=item.product,order_id=instance.order_id)
            if query_set:
                for i in query_set:
                    i.address=instance.address
                    i.city=instance.city
                    i.state=instance.state
                    i.save()
            else:
                SoldOrderItems.objects.create(item=item.product.title,quantity=item.quantity,timestamp=timestamp,order_id=instance.order_id,address=instance.address,city=instance.city,state=instance.state,sold_by=item.product.sold_by.user.username)



post_save.connect(post_save_create_soldorder,sender=Order)



def post_save_update_orderStatus(sender,instance,*args,**kwargs):
    order_id=instance.order_id
    sold_queryset=SoldOrderItems.objects.filter(status='PENDING',order_id=order_id)
    count=0
    for i in sold_queryset:
        count+=1
    if count==0:
        query=Order.objects.get(order_id=order_id)
        query.status='delivered'
        query.save()

post_save.connect(post_save_update_orderStatus,sender=SoldOrderItems)



def post_delete_update_SoldOrder(sender,instance,*args,**kwargs):
    order_id=instance.order_id
    query_set=SoldOrderItems.objects.filter(order_id=instance.order_id)
    for i in query_set:
        i.delete()

post_delete.connect(post_delete_update_SoldOrder,sender=Order)