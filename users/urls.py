from django.urls import path

from . import views

urlpatterns = [
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    path('logout', views.logout, name='logout'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('enroll_and_pay/<int:course_id>', views.enroll_and_pay, name='enroll_and_pay'),
    path('refund-request', views.refund_request, name='refund_request'),
    path('payment_history', views.payment_history, name='payment_history'),

]
   
