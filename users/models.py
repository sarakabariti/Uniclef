from __future__ import unicode_literals
from django.contrib.auth.models import AbstractUser
from django_countries.fields import CountryField
from django.db import models
from datetime import datetime
from django.conf import settings
from .managers import UserManager
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    GENDER_CHOICES = (
            ('male', 'Male'),
            ('female', 'Female'),
            ('other', 'Other'),
        )
    email = models.EmailField(_('email'), unique=True)
    phone_number = models.CharField(max_length=20)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    city = models.CharField(max_length=100)
    country_code = CountryField(settings.AUTH_USER_MODEL)
    profile_pic = models.ImageField(upload_to='photos/%Y/%m/%d', blank=True, null=True)
    date_joined = models.DateTimeField(default=datetime.now)
    last_active = models.DateTimeField(default=datetime.now, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name', 'country_code']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')