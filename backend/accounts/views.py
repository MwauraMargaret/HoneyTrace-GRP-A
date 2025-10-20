from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_otp.plugins.otp_totp.models import TOTPDevice
from .utils import generate_qr_image_base64, gen_backup_codes, hash_code
from .models import BackupCode
from rest_framework import status
from django.contrib.auth import get_user_model
import pyotp

User = get_user_model()

class TOTPSetupView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        # create an unconfirmed device
        # use name to allow multiple devices
        device = TOTPDevice.objects.create(user=user, confirmed=False, name="default")
        # get provisioning URI (otpauth)
        secret = device.bin_key  # bytes
        # pyotp uses base32 secret, but device.key is binary; easiest: make pyotp TOTP with device.config_url if available
        # Device has config_url on some versions; if not, build manually:
        try:
            otpauth_url = device.config_url
        except Exception:
            b32 = pyotp.random_base32()  # fallback (not ideal)
            otpauth_url = pyotp.totp.TOTP(b32).provisioning_uri(name=user.email, issuer_name="AsaliTrace")
        qr_data = generate_qr_image_base64(otpauth_url)
        # persist device id in response so client can confirm
        return Response({"otpauth_url": otpauth_url, "qr": qr_data, "device_id": device.persistent_id})

class TOTPConfirmView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        token = request.data.get("token")
        device_id = request.data.get("device_id")
        if not token or not device_id:
            return Response({"detail": "Missing"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            device = TOTPDevice.objects.get(persistent_id=device_id, user=request.user)
        except TOTPDevice.DoesNotExist:
            return Response({"detail": "Device not found"}, status=404)
        # verify token
        if device.verify_token(token):
            device.confirmed = True
            device.save()
            # generate backup codes, store hashed
            codes = gen_backup_codes()
            for c in codes:
                BackupCode.objects.create(user=request.user, code_hash=hash_code(c))
            return Response({"backup_codes": codes})
        else:
            return Response({"detail": "Invalid token"}, status=400)

class TOTPVerifyView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        # used during login second step; client sends email + token or user id + token
        identifier = request.data.get("identifier")  # email or username
        token = request.data.get("token")
        # lookup user
        if not identifier or not token:
            return Response({"detail": "Missing"}, status=400)
        try:
            user = User.objects.get(email=identifier)
        except User.DoesNotExist:
            return Response({"detail": "Invalid user"}, status=404)
        # check TOTP devices
        devices = TOTPDevice.objects.filter(user=user, confirmed=True)
        for d in devices:
            if d.verify_token(token):
                # create JWT for user and return (we recommend server create cookie; here return tokens)
                from rest_framework_simplejwt.tokens import RefreshToken
                refresh = RefreshToken.for_user(user)
                return Response({"access": str(refresh.access_token), "refresh": str(refresh)}, status=200)
        # check backup codes
        hashed = hash_code(token)
        try:
            bc = BackupCode.objects.get(user=user, code_hash=hashed, used=False)
            bc.used = True
            bc.save()
            from rest_framework_simplejwt.tokens import RefreshToken
            refresh = RefreshToken.for_user(user)
            return Response({"access": str(refresh.access_token), "refresh": str(refresh)}, status=200)
        except BackupCode.DoesNotExist:
            return Response({"detail": "Invalid token"}, status=400)