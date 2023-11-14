from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import gettext_lazy as _

from .models import User, Enrollment, Refund, StudentProgress, PaymentMethod


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
    list_display = ('id','course_id', 'user_id', 'enrolled_at', 'amount_paid')
    list_display_links = ('id','course_id', 'user_id')
    search_fields = ('id','course_id', 'user_id')
    list_per_page = 25

@admin.register(Refund)
class RefundAdmin(admin.ModelAdmin):
    list_display = ('id','enrollment_id', 'request_date', 'status')
    list_display_links = ('id','enrollment_id')
    search_fields = ('enrollment_id', 'request_date', 'status')
    list_per_page = 25

@admin.register(StudentProgress)
class StudentProgress(admin.ModelAdmin):
    list_display = ('id','enrollment_id', 'total_tasks', 'remaining_tasks', 'total_score')
    list_display_links = ('id','enrollment_id')
    search_fields = ('enrollment_id', 'total_score')
    list_per_page = 25

@admin.register(PaymentMethod)
class PaymentMethod(admin.ModelAdmin):
    list_display = ('id','user_id', 'payment_type', 'expiration_month', 'expiration_year')
    list_display_links = ('id','user_id')
    search_fields = ('id','user_id', 'payment_type')
    list_per_page = 25



