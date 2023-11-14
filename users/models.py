from __future__ import unicode_literals
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django_countries.fields import CountryField
from django.db import models, IntegrityError
from datetime import datetime
from django.conf import settings
from .managers import UserManager
from django.utils.translation import gettext_lazy as _

from django.core.validators import MinValueValidator, MaxValueValidator

from courses.models import Course

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

class Enrollment(models.Model):
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE) 
    enrolled_at = models.DateTimeField(default=datetime.now, blank=True)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method_id = models.ForeignKey('PaymentMethod', on_delete=models.DO_NOTHING)
    refunded = models.BooleanField(default=False)
    
    class Meta:
        indexes = [
            models.Index(fields=['user_id', 'course_id']),
        ]
'''
class Review(models.Model):
    enrollment_id = models.ForeignKey(Enrollment, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    review = models.TextField(blank=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                name='check_valid_rating',
                check=models.Q(rating__gte=1, rating__lte=5),
                message='Rating must be between 1 and 5.',
            ),
        ]

    def save(self, *args, **kwargs):
        # Ensure the rating is within the valid range before saving
        if not (1 <= self.rating <= 5):
            raise IntegrityError('Rating must be between 1 and 5.')
        super().save(*args, **kwargs)
'''

class Refund(models.Model):
    enrollment_id = models.ForeignKey(Enrollment, on_delete=models.DO_NOTHING, null=True)
    request_date = models.DateTimeField(default=datetime.now)
    reason = models.TextField()
    status = models.CharField(max_length=50)
    def _str_(self):
        return self.enrollment_id

class StudentProgress(models.Model):
    enrollment_id = models.ForeignKey(Enrollment, on_delete=models.CASCADE)
    total_tasks = models.PositiveIntegerField()
    remaining_tasks = models.PositiveIntegerField()
    total_score = models.PositiveIntegerField()

    class Meta:
        indexes = [
            models.Index(fields=['enrollment_id']),
        ]
class PaymentMethod(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_type = models.CharField(max_length=20,verbose_name=_("Payment Type"))
    card_number = models.CharField(max_length=16, verbose_name=_("Card Number"))
    cardholder_name = models.CharField(max_length=255, verbose_name=_("Cardholder Name"))
    expiration_month = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(12)],
    verbose_name=_("Expiration Month"))
    expiration_year = models.PositiveSmallIntegerField(validators=[MinValueValidator(2023)],
    verbose_name=_("Expiration Year"))
