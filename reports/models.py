from django.conf import settings
from django.db import models

from services.models import Service


class Report(models.Model):
    """A user-submitted report: incorrect place info, an app bug, or a
    suggestion. Integer auto-PK (id). The reporter and the related service
    are optional so anonymous / app-level reports are still stored."""

    class ReportType(models.TextChoices):
        INCORRECT_INFO = 'incorrect_info', 'Incorrect information'
        BUG = 'bug', 'App bug'
        SUGGESTION = 'suggestion', 'Suggestion'

    class ReportStatus(models.TextChoices):
        PENDING = 'pending', 'Pending'
        INVESTIGATING = 'investigating', 'Investigating'
        RESOLVED = 'resolved', 'Resolved'
        DISMISSED = 'dismissed', 'Dismissed'

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='reports')
    service = models.ForeignKey(
        Service, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='reports')
    report_type = models.CharField(
        max_length=20, choices=ReportType.choices, default=ReportType.INCORRECT_INFO)
    message = models.TextField()
    status = models.CharField(
        max_length=20, choices=ReportStatus.choices, default=ReportStatus.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'reports'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.report_type} #{self.pk}'
