from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import *
from phonenumber_field.modelfields import *

# Create your models here.

CHOICE_ROLE = (('bakery_admin', 'bakery_admin'), ('customer', 'customer'))


class UserProfileModel(AbstractUser):
    role_type = models.CharField(max_length=20,choices=CHOICE_ROLE, default='superadmin')
    phone_number = PhoneNumberField(unique=True, default='0')
    email = models.EmailField(unique=True, validators=[EmailValidator])
    activation_link = models.URLField(default='0')
