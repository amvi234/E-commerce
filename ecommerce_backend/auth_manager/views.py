import pyotp
from django.contrib.auth import authenticate
from django_otp.plugins.otp_totp.models import TOTPDevice
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

# from ecommerce_backend.shared.exception_handling.api_exceptions import AuthException
# from shared.exception_handling import ApiErrors


class AuthViewSet(ViewSet):
    @action(
        detail=False,
        methods=["post"],
    )
    def login(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)
        if not user:
            return Response({"message": "Invalid credentials"}, status=400)
            # raise AuthException(
            #     ApiErrors.AUTHENTICATION_FAILED.value,
            # )

        totp_device, _ = TOTPDevice.objects.get_or_create(user=user, confirmed=True)
        otp = pyotp.TOTP(totp_device.key).now()

        response = {
            "message": "User logged in successfully.",
            "data": {"otp_secret": totp_device.key, "otp": otp, "message": "Enter OTP"},
        }

        return Response(response)
