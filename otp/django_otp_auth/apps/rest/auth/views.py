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
                    'message': 'The temporary password has been sent',
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
                return Response(self._handle_login(data, request))
            else:
                return Response(err_msg('sent code is incorrect', 400),
                                status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response(err_msg('equest is invalid', 400),
                            status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def _handle_login(otp, rqt):
        receiver = otp.get('receiver')
        otp_uuid = otp.get('uuid')
        otp_code_value = otp.get('code')

        if not all([receiver, otp_uuid, otp_code_value]):
            raise ValueError("OTP data is incomplete.")
        
        with transaction.atomic():
            try:
                user = User.objects.get(
                    mobile_number=receiver
                )
            except User.DoesNotExist:
                user = User.objects.create(
                    mobile_number=receiver,
                    email=None,
                    username=User.generate_username()
                )

            try:
                otp_code = OTPCode.objects.get(receiver=receiver, uuid=otp_uuid, code=otp_code_value)
                # Mark the OTP code as used
                otp_code.used = True
                otp_code.save()
            except OTPCode.DoesNotExist:
                pass

            user.last_login = timezone.now()
            user.save()

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
