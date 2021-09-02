from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
import uuid
# Create your models here.

class UserManager(BaseUserManager):
    use_in_migrations = True
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        return self.create_user(email, password, **extra_fields)



class User(AbstractUser):
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=14)
    otp = models.IntegerField(null=True, blank=True)
    is_verified = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

class Address(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    address_user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=50)
    mobile = models.CharField(max_length=14)
    address = models.CharField(max_length=250)
    city = models.CharField(max_length=50)
    district = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    pincode = models.IntegerField()
    address_type = models.CharField(max_length=10)
    default = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Address"
        verbose_name_plural = "Addresses"
    
    def __str__(self):
        return self.full_name
    