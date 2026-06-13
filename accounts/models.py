import secrets

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models


class AppUserManager(BaseUserManager):
    def create_user(self, phone_hash, display_name='User', **extra_fields):
        if not phone_hash:
            raise ValueError('The phone_hash must be set')
        user = self.model(phone_hash=phone_hash, display_name=display_name, **extra_fields)
        # Auth is via OTP — users never have a usable password.
        user.set_unusable_password()
        user.save(using=self._db)
        return user


class AppUser(AbstractBaseUser):
    """Project-owned user table — Django's default auth_user is not used."""

    # Integer auto-PK (id) is added by Django; phone_hash stays the unique
    # login identifier but is no longer the primary key.
    phone_hash = models.CharField(max_length=255, unique=True)
    display_name = models.CharField(max_length=255, default='User')
    avatar_url = models.URLField(max_length=1024, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    # Admins may create/edit/delete service (government place) records.
    is_admin = models.BooleanField(default=False)

    objects = AppUserManager()

    USERNAME_FIELD = 'phone_hash'
    REQUIRED_FIELDS = []

    class Meta:
        db_table = 'users'

    def __str__(self):
        return f"{self.display_name} ({self.phone_hash[:8]}...)"


class OtpCode(models.Model):
    """One-time codes sent to a phone number during login."""

    phone = models.CharField(max_length=20, db_index=True)
    code = models.CharField(max_length=6)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'otp_codes'

    def __str__(self):
        return f"OTP for {self.phone}"


class AuthToken(models.Model):
    """Project-owned API token table (replaces rest_framework.authtoken)."""

    key = models.CharField(max_length=64, primary_key=True)
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE, related_name='tokens')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'auth_tokens'

    @classmethod
    def issue(cls, user):
        return cls.objects.create(key=secrets.token_hex(32), user=user)

    def __str__(self):
        return f"Token for {self.user_id}"
