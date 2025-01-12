from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
# Create your models here.

class CustomUserManager(BaseUserManager):

    def create(self, email, password=None, **extra_fields):
        """
        Create and return a regular user with an email, first_name, last_name, and password.
        """
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create and return a superuser with an email password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create(email, password, **extra_fields)

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