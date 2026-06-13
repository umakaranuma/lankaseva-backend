from django.db.models import F
from django.utils import timezone
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from .models import Review
from .serializers import ReviewSerializer


class IsOwnerOrReadOnly(permissions.BasePermission):
    """Only the review's author may edit or delete it."""

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user_id == request.user.pk


from config.permissions import IsOwnerOrAdminOrReadOnly

class ReviewViewSet(viewsets.ModelViewSet):
    """
    Public API for viewing reviews; writes require authentication.

    Query params: service, district, stars, user=me (own reviews).
    """

    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrAdminOrReadOnly]

    def get_queryset(self):
        queryset = (
            Review.objects.select_related('user', 'service')
            .prefetch_related('tags')
            .order_by('-created_at')
        )
        params = self.request.query_params

        service_id = params.get('service')
        district = params.get('district')
        stars = params.get('stars')

        if service_id:
            queryset = queryset.filter(service_id=service_id)
        if district:
            queryset = queryset.filter(service__district__iexact=district)
        if stars:
            queryset = queryset.filter(stars=stars)
        if params.get('user') == 'me' and self.request.user.is_authenticated:
            queryset = queryset.filter(user=self.request.user)
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(edited_at=timezone.now())

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def helpful(self, request, pk=None):
        review = self.get_object()
        Review.objects.filter(pk=review.pk).update(helpful_count=F('helpful_count') + 1)
        review.refresh_from_db(fields=['helpful_count'])
        return Response({'status': 'helpful vote registered', 'helpful_count': review.helpful_count})
