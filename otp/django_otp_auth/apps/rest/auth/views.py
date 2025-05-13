import datetime

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView
from django.utils import timezone
from django.db import transaction
from rest_framework.permissions import AllowAny

from django_otp_auth.apps.rest.auth.serializers import RequestOTPSerializer, VerifyOtpRequestSerializer, ObtainTokenSerializer
from django_otp_auth.apps.base.user.models import OTPCode
from django_otp_auth.apps.rest.core.utils import err_msg, err_serializer

User = get_user_model()


class OTPCreateView(APIView):
    queryset = OTPCode.objects.all()
    permission_classes = [
        AllowAny,
    ]

    def post(self, request):
        serializer = RequestOTPSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            try:
                otp = OTPCode.objects.generate(data)
                print(otp.code)
                return Response(data={
                    'uuid': otp.uuid,
                    'receiver': otp.receiver,
                    'message': 'رمز عبور موقت ارسال شد',
                }, status=status.HTTP_200_OK)
            except Exception as e:
                print(e)
                return Response(err_msg('Error connecting to the server', 500),
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(err_msg(err_serializer(serializer.errors), 400), status=status.HTTP_400_BAD_REQUEST)


class OTPVerifyView(APIView):
    queryset = OTPCode.objects.all()
    permission_classes = [
        AllowAny,
    ]

    def post(self, request):
        serializer = VerifyOtpRequestSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            if OTPCode.objects.is_valid(data['receiver'], data['uuid'], data['code']):
                response_data = self._handle_login(data, request)
                print(response_data)
                return Response(response_data)
            return Response(err_msg('کد ارسال شده درست نمیباشد', 400), status=status.HTTP_400_BAD_REQUEST)

        return Response(err_msg(err_serializer(serializer.errors), 400), status=status.HTTP_400_BAD_REQUEST)

    def _handle_login(self, otp_data, request):
        """
        Main login workflow: get/create user, validate OTP, issue tokens.
        """
        with transaction.atomic():
            user = self._get_or_create_user(otp_data['receiver'])
            self._mark_otp_as_used(otp_data)
            self._finalize_user(user)

        return self._generate_tokens(user)
    
    def _get_or_create_user(self, mobile_number):
        """
        Returns existing user by mobile number or creates a new one.
        """
        try:
            user = User.objects.get(
                mobile_number=mobile_number
            )
        except User.DoesNotExist:
            user = User.objects.create(
                mobile_number=mobile_number,
                email=None,
                username=User.generate_username()
            )
        return user
    
    def _mark_otp_as_used(self, otp_data):
        """
        Marks the matching OTP code as used.
        """
        try:
            otp_code = OTPCode.objects.get(
                receiver=otp_data['receiver'],
                uuid=otp_data['uuid'],
                code=otp_data['code']
            )
            otp_code.used = True
            otp_code.save()
        except OTPCode.DoesNotExist as e:
            print(f"Error: {e}")

    def _finalize_user(self, user):
        """
        Updates last login.
        """
        user.last_login = timezone.now()
        user.save()
    
    def _generate_tokens(self, user):
        """
        Returns new access and refresh tokens for user.
        """
        access = AccessToken.for_user(user=user)
        access.set_exp(lifetime=datetime.timedelta(minutes=30))
        refresh = RefreshToken.for_user(user=user)
        return ObtainTokenSerializer({
            'access': str(access),
            'refresh': str(refresh)
        }).data


# permission_cls =
otp_create_code = OTPCreateView.as_view()
otp_refresh_jwt = TokenRefreshView.as_view()
otp_verify_code = OTPVerifyView.as_view()
