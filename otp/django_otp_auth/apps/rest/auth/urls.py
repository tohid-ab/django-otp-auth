from django.urls import path

from . import views

urlpatterns = [
    path('otp/create/', views.otp_create_code),
    path('otp/refresh/', views.otp_refresh_jwt),
    path('otp/verify/', views.otp_verify_code),
]
