from rest_framework import serializers

from .models import AppUser


class AppUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppUser
        fields = ['id', 'phone_hash', 'display_name', 'avatar_url', 'created_at']
        read_only_fields = ['id', 'phone_hash', 'created_at']
