# Create your models here.
from django.urls import reverse
from django.db import models
# from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from .utils import unique_slug_generator
from model_utils import FieldTracker



from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):

    SUPERUSER = 1
    FARMER = 2
    CUSTOMER = 3

    USER_TYPE_CHOICES = (
        (SUPERUSER, 'superuser'),
        (FARMER, 'farmer'),
        (CUSTOMER, 'customer'),
    )
    username=models.CharField(_('username'),unique=True,max_length=20)
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    is_active = models.BooleanField(_('active'), default=True)
    is_staff = models.BooleanField(default=False)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    user_type=models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES,default=3,blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        '''
        Returns the short name for the user.
        '''
        return self.first_name

    # def email_user(self, subject, message, from_email=None, **kwargs):
    #     '''
    #     Sends an email to this User.
    #     '''
    #     send_mail(subject, message, from_email, [self.email], **kwargs)


class Farmer(models.Model):
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name="farm_profile")
    address=models.TextField(blank=True,default="")
    city=models.CharField(max_length=20,blank=True,default="")
    state=models.CharField(max_length=20,blank=True,default="")
    company_name=models.CharField(max_length=100,blank=True,default="")


    # def update(self):
    #     Farmer.object.filter(pk=self.id).update(slug=unique_slug_generator(self))

    def __str__(self):
        return f'{self.user.username}'

    def get_absolute_url(self):
        """
        Returns the url to access a particular instance of Product.
        """
        return reverse('farmer-detail-view', args=[str(self.user.username)])

    @property
    def full_name(self):
        return f'{self.user.first_name} {self.user.last_name}'

    @property
    def username(self):
        return self.user.username

# @receiver(post_save, sender=Farmer)
# def generate_unique_slug_for_farmers(sender, instance, created, *args, **kwargs):

#         if created:
#             slug = unique_slug_generator(instance)
#             Farmer.object.create(slug=slug,**kwargs)
#             # instance.save()
#         # instance.save()














class Customer(models.Model):
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name="cust_profile")
    address=models.TextField(blank=True,default="")
    city=models.CharField(max_length=20,blank=True,default="")
    state=models.CharField(max_length=20,blank=True,default="")


    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

    def get_absolute_url(self):

        return reverse('customer-detail-view', args=[str(self.id)])

    @property
    def full_name(self):
        return f'{self.user.first_name} {self.user.last_name}'

    @property
    def username(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, *args, **kwargs):
    """Automatically Create A User Profile When A New User IS Registered"""

    if created:
        if instance.user_type==2:
            user_profile = Farmer(user=instance)
            user_profile.save()
        if instance.user_type==3:
            user_profile = Customer(user=instance)
            user_profile.save()



class Land(models.Model):
    user=models.ForeignKey(Farmer,on_delete=models.CASCADE,related_name='lands')
    city=models.CharField(max_length=255,blank=True, null=True)
    latitude=models.FloatField(max_length=255,blank=True, null=True)
    longitude=models.FloatField(max_length=255,blank=True, null=True)

    @property
    def name(self):
        return self.city+" "+self.username

    @property
    def username(self):
        return self.user.username

