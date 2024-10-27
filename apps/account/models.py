import re

from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, UserManager


# Create your models here.
class ManagerUserManager(BaseUserManager):
    def create_user(self, phone_number=None, password=None, **extra_fields):
        if not phone_number:
            raise ValueError('Phone number must be set')
        user = self.model(phone_number=phone_number, **extra_fields)
        pattern_validator = re.compile(r'^((?=\S*?[A-Z])(?=\S*?[a-z])(?=\S*?[0-9]).{6,})\S$')
        if not pattern_validator.match(password):
            raise ValueError('Invalid password')
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        return self.create_user(phone_number, password, **extra_fields)

    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class User(AbstractUser):
    phone_number = models.CharField(max_length=11, unique=True)
    name = models.CharField(max_length=20, null=True, blank=True)
    image = models.ImageField(upload_to='profile/', null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)
    username = None

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['email']
    objects = ManagerUserManager()

    def __str__(self):
        return self.phone_number
