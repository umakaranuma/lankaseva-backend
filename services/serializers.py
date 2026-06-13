from django.db import transaction
from rest_framework import serializers

from .models import OpeningHourSlot, OpeningHours, Service, ServicePhone, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ServicePhoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServicePhone
        fields = ['label_en', 'label_si', 'label_ta', 'number', 'is_primary']


class OpeningHourSlotSerializer(serializers.ModelSerializer):
    open = serializers.TimeField(source='open_time', format='%H:%M')
    close = serializers.TimeField(source='close_time', format='%H:%M')

    class Meta:
        model = OpeningHourSlot
        fields = ['weekday', 'open', 'close']

    def validate(self, attrs):
        if attrs['close_time'] <= attrs['open_time']:
            raise serializers.ValidationError('close must be after open.')
        return attrs


class OpeningHoursSerializer(serializers.ModelSerializer):
    days = OpeningHourSlotSerializer(source='slots', many=True, required=False)

    class Meta:
        model = OpeningHours
        fields = ['is_always_open', 'notes', 'days']

    def validate(self, attrs):
        slots = attrs.get('slots', [])
        weekdays = [s['weekday'] for s in slots]
        if len(weekdays) != len(set(weekdays)):
            raise serializers.ValidationError({'days': 'Duplicate weekday entries.'})
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
            self._save_hours(service, hours)
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
            self._save_hours(instance, hours)
        # Re-fetch so the response reflects the replaced phones/hours rather
        # than the relation caches loaded before the update.
        return (Service.objects.select_related('hours')
                .prefetch_related('phones', 'hours__slots').get(pk=instance.pk))

    @staticmethod
    def _save_phones(service, phones):
        ServicePhone.objects.bulk_create(
            [ServicePhone(service=service, **phone) for phone in phones]
        )

    @staticmethod
    def _save_hours(service, hours):
        slots = hours.pop('slots', [])
        record, _ = OpeningHours.objects.update_or_create(
            service=service,
            defaults={'is_always_open': hours.get('is_always_open', False),
                      'notes': hours.get('notes')},
        )
        record.slots.all().delete()
        OpeningHourSlot.objects.bulk_create(
            [OpeningHourSlot(hours=record, **slot) for slot in slots]
        )
