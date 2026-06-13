from rest_framework import serializers

from .models import EmergencyHotline


class EmergencyHotlineSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmergencyHotline
        fields = ['name_key', 'number', 'icon_key', 'color',
                  'is_quick_dial', 'sort_order']
