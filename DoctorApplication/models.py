from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
# Create your models here.

class CustomUserManager(BaseUserManager):
    pass

class CustomUser(AbstractBaseUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=False,null=False)
    last_name = models.CharField(max_length=30, blank=True,null=False)
    user_type = models.CharField(max_length=10,choices=(('doctor','doctor'),
                                                        ('staff','staff'),
                                                        ('patient','patient')),
                                default='patient',blank=False,null=False
                                )
    mobile = models.CharField(max_length=10,blank=True,null=True)
    date_of_birth = models.DateField(blank=True,null=True)                                                  
    date_registered = models.DateTimeField(auto_now_add=True)
    otp = models.IntegerField(blank=True,null=True)
    otp_expiry = models.DateTimeField(blank=True,null=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'custom_user'
        verbose_name_plural = 'custom_users'
        db_table = "custom_user"




# Create your models here.
