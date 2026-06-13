from rest_framework import serializers

from .models import Report


class ReportSerializer(serializers.ModelSerializer):
    # Echo the reporter's name on reads (left-join to the user table).
    user_id = serializers.IntegerField(source='user.id', read_only=True)
    display_name = serializers.CharField(source='user.display_name', read_only=True)
    service_name = serializers.CharField(source='service.name_en', read_only=True)

    class Meta:
        model = Report
        fields = ['id', 'user_id', 'display_name', 'service', 'service_name', 'report_type',
                  'message', 'status', 'created_at']
        read_only_fields = ['id', 'user_id', 'display_name', 'service_name', 'created_at']

    def validate_message(self, value):
        if not value.strip():
            raise serializers.ValidationError('Message cannot be empty.')
        return value
