from django.contrib.auth import get_user_model
from rest_framework import serializers

from django_otp_auth.apps.rest.core.utils import is_mobile_number

User = get_user_model()


class RequestOTPSerializer(serializers.Serializer):
    # Serializer for requesting an OTP code with mobile number validation

    receiver = serializers.CharField(required=True, max_length=13, min_length=10)

    @staticmethod
    def validate_receiver(value):
        if is_mobile_number(value):
            return value
        raise serializers.ValidationError("The mobile number is invalid")


class VerifyOtpRequestSerializer(serializers.Serializer):
    # Serializer for verifying an OTP code using UUID, mobile number, and verification code

    uuid = serializers.UUIDField(allow_null=False)
    receiver = serializers.CharField(max_length=64, allow_null=False)
    code = serializers.CharField(max_length=5, allow_null=False)


class ObtainTokenSerializer(serializers.Serializer):
    # Serializer for obtaining access and refresh tokens

    access = serializers.CharField(max_length=255, allow_null=False)
    refresh = serializers.CharField(max_length=255, allow_null=False)
