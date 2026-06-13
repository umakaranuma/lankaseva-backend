from rest_framework import viewsets

from config.permissions import IsAdminOrReadOnly

from .models import EmergencyHotline
from .serializers import EmergencyHotlineSerializer


class EmergencyHotlineViewSet(viewsets.ModelViewSet):
    """
    National emergency hotlines.

    Reads are public; create / edit / delete require an admin token — the
    same RESTful shape as the services resource:

        GET    /api/emergency/        list (use ?quick=true for quick-dial)
        POST   /api/emergency/        create
        GET    /api/emergency/{id}/   retrieve one
        PUT    /api/emergency/{id}/   replace
        PATCH  /api/emergency/{id}/   partial update
        DELETE /api/emergency/{id}/   delete

    The list stays unpaginated (small fixed reference set) so clients can
    read it as a plain array.
    """

    serializer_class = EmergencyHotlineSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = None

    def get_queryset(self):
        queryset = EmergencyHotline.objects.all()
        if self.request.query_params.get('quick', '').lower() in ('1', 'true', 'yes'):
            queryset = queryset.filter(is_quick_dial=True)
        return queryset
