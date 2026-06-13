from django.db import transaction
from rest_framework import serializers

from .models import Review, ReviewTag

class ReviewTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewTag
        fields = ['tag_key', 'is_positive']

class ReviewSerializer(serializers.ModelSerializer):
    tags = ReviewTagSerializer(many=True, read_only=True)
    # Left-join to the user table: the reviewer's integer id + their name.
    user_id = serializers.IntegerField(source='user.id', read_only=True)
    display_name = serializers.CharField(source='user.display_name', read_only=True)
    # Place name carried alongside the service id for convenience on reads.
    service_name = serializers.CharField(source='service.name_en', read_only=True)

    stars = serializers.IntegerField(min_value=1, max_value=5)
    positive_tags = serializers.ListField(
        child=serializers.CharField(max_length=100), write_only=True, required=False
    )
    negative_tags = serializers.ListField(
        child=serializers.CharField(max_length=100), write_only=True, required=False
    )

    class Meta:
        model = Review
        fields = [
            'id', 'service', 'service_name', 'user_id', 'display_name',
            'stars', 'text', 'helpful_count', 'created_at', 'edited_at',
            'tags', 'positive_tags', 'negative_tags'
        ]
        read_only_fields = ['id', 'service_name', 'user_id', 'display_name',
                            'helpful_count', 'created_at', 'edited_at']

    @transaction.atomic
    def create(self, validated_data):
        positive_tags = validated_data.pop('positive_tags', [])
        negative_tags = validated_data.pop('negative_tags', [])

        review = Review.objects.create(**validated_data)

        for tag in positive_tags:
            ReviewTag.objects.create(review=review, tag_key=tag, is_positive=True)
        for tag in negative_tags:
            ReviewTag.objects.create(review=review, tag_key=tag, is_positive=False)

        return review

    @transaction.atomic
    def update(self, instance, validated_data):
        positive_tags = validated_data.pop('positive_tags', None)
        negative_tags = validated_data.pop('negative_tags', None)

        instance = super().update(instance, validated_data)

        if positive_tags is not None or negative_tags is not None:
            instance.tags.all().delete()
            for tag in positive_tags or []:
                ReviewTag.objects.create(review=instance, tag_key=tag, is_positive=True)
            for tag in negative_tags or []:
                ReviewTag.objects.create(review=instance, tag_key=tag, is_positive=False)
        return instance
