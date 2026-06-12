import re

from django.db import transaction
from rest_framework import serializers

from .models import OpeningHours, Service, ServicePhone

DAY_RANGE_RE = re.compile(r'^\d{2}:\d{2}-\d{2}:\d{2}$')


class ServicePhoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServicePhone
        fields = ['label_en', 'label_si', 'label_ta', 'number', 'is_primary']


class OpeningHoursSerializer(serializers.ModelSerializer):
    class Meta:
        model = OpeningHours
        exclude = ['id', 'service']

    def validate(self, attrs):
        for day in ('mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun'):
            value = attrs.get(day)
            if value and not DAY_RANGE_RE.match(value):
                raise serializers.ValidationError(
                    {day: 'Must be "HH:MM-HH:MM" or null for closed.'})
        return attrs


class ServiceSerializer(serializers.ModelSerializer):
    """Full service payload — one document per place, exactly as the mobile
    single-view UI shows it: names/department/address in three languages,
    location, phone list and weekly opening hours.

    Writes accept the same nested shape, so admins store/edit a place with a
    single request.
    """

    phones = ServicePhoneSerializer(many=True, required=False)
    hours = OpeningHoursSerializer(required=False)

    class Meta:
        model = Service
        fields = '__all__'

    def validate_phones(self, phones):
        if self.instance is None and not phones:
            raise serializers.ValidationError('At least one phone number is required.')
        if phones and sum(1 for p in phones if p.get('is_primary')) > 1:
            raise serializers.ValidationError('Only one phone can be primary.')
        return phones

    @transaction.atomic
    def create(self, validated_data):
        phones = validated_data.pop('phones', [])
        hours = validated_data.pop('hours', None)

        service = Service.objects.create(**validated_data)
        self._save_phones(service, phones)
        if hours is not None:
            OpeningHours.objects.create(service=service, **hours)
        return service

    @transaction.atomic
    def update(self, instance, validated_data):
        phones = validated_data.pop('phones', None)
        hours = validated_data.pop('hours', None)

        instance = super().update(instance, validated_data)

        if phones is not None:  # full replacement, like the edit form submits
            instance.phones.all().delete()
            self._save_phones(instance, phones)
        if hours is not None:
            OpeningHours.objects.update_or_create(service=instance, defaults=hours)
        return instance

    @staticmethod
    def _save_phones(service, phones):
        ServicePhone.objects.bulk_create(
            [ServicePhone(service=service, **phone) for phone in phones]
        )
