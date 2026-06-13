from rest_framework import permissions
from rest_framework.generics import ListAPIView

from .models import EmergencyHotline
from .serializers import EmergencyHotlineSerializer


class EmergencyHotlineList(ListAPIView):
    """Public, unpaginated list of all hotlines (ordered by sort_order).

    Pass ?quick=true for just the home-screen quick-dial tiles.
    """

    serializer_class = EmergencyHotlineSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = None

    def get_queryset(self):
        queryset = EmergencyHotline.objects.all()
        if self.request.query_params.get('quick', '').lower() in ('1', 'true', 'yes'):
            queryset = queryset.filter(is_quick_dial=True)
        return queryset
