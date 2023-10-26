from __future__ import unicode_literals
from django.contrib.auth.models import AbstractBaseUser
from django_countries.fields import CountryField
from django.db import models
from datetime import datetime
from django.conf import settings
from .managers import UserManager
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import PermissionsMixin

class User(AbstractBaseUser, PermissionsMixin):
    GENDER_CHOICES = (
            ('male', 'Male'),
            ('female', 'Female'),
            ('other', 'Other'),
        )
    first_name = models.CharField(_('first_name'), max_length=30, blank=True)
    last_name = models.CharField(_('last_name'), max_length=30, blank=True)
    email = models.EmailField(_('email'), unique=True)
    phone_number = models.CharField(max_length=20)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    city = models.CharField(max_length=100)
    country_code = CountryField(settings.AUTH_USER_MODEL)
    profile_pic = models.ImageField(upload_to='photos/%Y/%m/%d', blank=True, null=True)
    date_joined = models.DateTimeField(default=datetime.now)
    last_active = models.DateTimeField(default=datetime.now, blank=True)
    is_staff = models.BooleanField(_("staff status"), default=False, help_text=_("Designates whether the user can log into this admin site."),)
    is_active = models.BooleanField(_("active"),default=True,help_text=_("Designates whether this user should be treated as active. ""Unselect this instead of deleting accounts."),)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        