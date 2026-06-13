from rest_framework import mixins, permissions, viewsets

from config.permissions import IsAdmin

from .models import Report
from .serializers import ReportSerializer


class ReportViewSet(mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    viewsets.GenericViewSet):
    """
    Store user reports.

        POST   /api/reports/        submit a report (anyone)
        GET    /api/reports/        list reports (admin only)
        GET    /api/reports/{id}/   one report (admin only)

    Reports are write-only for normal users; reading them is an admin task.
    """

    serializer_class = ReportSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.AllowAny()]
        return [IsAdmin()]

    def get_queryset(self):
        return Report.objects.select_related('user', 'service').all()

    def perform_create(self, serializer):
        # Attach the signed-in user when there is one; otherwise anonymous.
        user = self.request.user if self.request.user.is_authenticated else None
        serializer.save(user=user)
