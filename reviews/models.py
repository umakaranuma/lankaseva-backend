from django.db import models
from django.conf import settings
from services.models import Service

class Review(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews')
    
    stars = models.IntegerField()
    text = models.TextField()
    helpful_count = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'reviews'

    def __str__(self):
        return f"Review by {self.user.display_name} for {self.service.name_en}"


class ReviewTag(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='tags')
    tag_key = models.CharField(max_length=100)
    is_positive = models.BooleanField()

    class Meta:
        db_table = 'review_tags'

    def __str__(self):
        return f"{self.tag_key} ({'Positive' if self.is_positive else 'Negative'})"
