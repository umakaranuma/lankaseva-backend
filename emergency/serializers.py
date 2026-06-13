from rest_framework import serializers

from .models import EmergencyHotline


class EmergencyHotlineSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmergencyHotline
        fields = ['id', 'name_key', 'number', 'icon_key', 'color',
                  'is_quick_dial', 'sort_order']
        read_only_fields = ['id']
