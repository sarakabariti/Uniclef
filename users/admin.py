from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import gettext_lazy as _

from .models import User, Enrollment, Refund, StudentProgress, PaymentMethod, PaymentHistory


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    """Define admin model for custom User model with no email field."""

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password'),
        }),
    )

    list_filter = ('is_active', 'is_staff')
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'last_login')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('course_id', 'user_id', 'enrolled_at', 'amount_paid')

@admin.register(Refund)
class RefundAdmin(admin.ModelAdmin):
    list_display = ('enrollment_id', 'request_date', 'status')

@admin.register(StudentProgress)
class StudentProgress(admin.ModelAdmin):
    list_display = ('enrollment_id', 'total_tasks', 'remaining_tasks', 'total_score')

@admin.register(PaymentMethod)
class PaymentMethod(admin.ModelAdmin):
    list_display = ('user_id', 'payment_type', 'expiration_month', 'expiration_year')

@admin.register(PaymentHistory)
class PaymentHistory(admin.ModelAdmin):
    list_display = ('enrollment_id', 'date', 'amount', 'status')


