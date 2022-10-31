from email.policy import default
from unittest.util import _MAX_LENGTH
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    def create_user(self, email, password, **other_fields):
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            **other_fields
        )
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, email, password, **other_fields):
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)
        other_fields.setdefault('is_admin', True)
        other_fields.setdefault('is_staff', True)
        
        if other_fields.get('is_staff') is not True:
                raise ValueError(_("Superuser should have is_staff as True"))
        if other_fields.get('is_superuser') is not True:
                raise ValueError(_("Superuser should have is_superuser as True"))
        if other_fields.get('is_active') is not True:
                raise ValueError(_("Superuser should have is_active as True"))
        if other_fields.get('is_admin') is not True:
                raise ValueError(_("Superuser should have is_admin as True"))
        
        user = self.create_user(email, password, **other_fields)
        return user
    
class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=255,default='')
    last_name = models.CharField(max_length=255,default='')
    email = models.EmailField(max_length=255, unique=True)
    phone = models.CharField(max_length=15, blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    shipping_address =models.TextField(default='nil')
    billing_address = models.CharField(max_length=300, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now = True, null=True, blank=True)
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS= ["first_name", "last_name", "phone"]
    
    objects = UserManager()
    
    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    
class Shop(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    slug = models.SlugField(null=True)
    facebook = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    whatsapp = models.URLField(blank=True)
    instagram = models.URLField(blank=True)
    about = models.TextField()
    banner = models.ImageField(upload_to='photos/%Y/%m/%d', blank=True)
    logo = models.ImageField(upload_to='photos/%Y/%m/%d', blank=True)
    info = models.TextField()  
    account_holder_name = models.CharField(max_length=255)
    account_number = models.CharField(max_length=255)
    account_holder_email = models.EmailField(max_length=255)
    bank_name = models.CharField(max_length=255)
    address_country = models.CharField(max_length=255)
    address_city = models.CharField(max_length=255)
    address_zip =models.CharField(max_length=255)
    street_address = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now = True, null=True, blank=True)
    "each shop has their wallet "
    wallet = models.DecimalField(max_digits=10, decimal_places=2,default=0.00)
    paystack_recipient = models.CharField(max_length=255, null=True)
    
    def __str__(self):
            return self.name
      
    
    
    
