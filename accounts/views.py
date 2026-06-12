import hashlib
import re
import secrets
from datetime import timedelta

from django.conf import settings
from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle
from rest_framework.views import APIView

from .models import AppUser, AuthToken, OtpCode
from .serializers import AppUserSerializer

PHONE_RE = re.compile(r'^7\d{8}$')  # Sri Lankan mobile, without +94


def normalize_phone(raw):
    """Accepts '7XXXXXXXX', '07XXXXXXXX' or '+947XXXXXXXX' → '+947XXXXXXXX'."""
    digits = re.sub(r'\D', '', raw or '')
    if digits.startswith('94'):
        digits = digits[2:]
    elif digits.startswith('0'):
        digits = digits[1:]
    if not PHONE_RE.match(digits):
        return None
    return f'+94{digits}'


def hash_phone(phone):
    return hashlib.sha256(phone.encode()).hexdigest()


class OtpThrottle(AnonRateThrottle):
    scope = 'otp'


class SendOTPView(APIView):
    authentication_classes = []
    throttle_classes = [OtpThrottle]

    def post(self, request):
        phone = normalize_phone(request.data.get('phone'))
        if not phone:
            return Response({'error': 'A valid Sri Lankan mobile number is required'},
                            status=status.HTTP_400_BAD_REQUEST)

        code = f'{secrets.randbelow(1000000):06d}'
        OtpCode.objects.filter(phone=phone, is_used=False).update(is_used=True)
        OtpCode.objects.create(
            phone=phone,
            code=code,
            expires_at=timezone.now() + timedelta(minutes=settings.OTP_EXPIRY_MINUTES),
        )

        # TODO: integrate an SMS gateway. Until then the code is returned in
        # DEBUG mode so the mobile app can be tested end-to-end.
        payload = {'message': 'OTP sent successfully'}
        if settings.DEBUG:
            payload['debug_otp'] = code
        return Response(payload)


class VerifyOTPView(APIView):
    authentication_classes = []
    throttle_classes = [OtpThrottle]

    def post(self, request):
        phone = normalize_phone(request.data.get('phone'))
        otp = (request.data.get('otp') or '').strip()
        if not phone or not otp:
            return Response({'error': 'phone and otp are required'},
                            status=status.HTTP_400_BAD_REQUEST)

        record = OtpCode.objects.filter(
            phone=phone, code=otp, is_used=False, expires_at__gt=timezone.now()
        ).first()
        if not record:
            return Response({'error': 'Invalid or expired OTP'},
                            status=status.HTTP_400_BAD_REQUEST)
        record.is_used = True
        record.save(update_fields=['is_used'])

        phone_hash = hash_phone(phone)
        user, created = AppUser.objects.get_or_create(
            phone_hash=phone_hash,
            defaults={'display_name': request.data.get('display_name') or 'User'},
        )
        token = AuthToken.issue(user)

        return Response({
            'token': token.key,
            'user': AppUserSerializer(user).data,
            'is_new_user': created,
        })


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(AppUserSerializer(request.user).data)

    def put(self, request):
        serializer = AppUserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # request.auth is the AuthToken row used for this request.
        if request.auth:
            request.auth.delete()
        return Response({'message': 'Logged out'})


class DeleteAccountView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        request.user.delete()  # cascades to tokens and reviews
        return Response(status=status.HTTP_204_NO_CONTENT)
