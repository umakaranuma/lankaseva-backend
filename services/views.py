from django.db.models import Q
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Service, ServiceCategory
from .serializers import ServiceSerializer


class IsAdminOrReadOnly(permissions.BasePermission):
    """Anyone can read; only users flagged is_admin may store/edit/delete."""

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(
            request.user
            and request.user.is_authenticated
            and getattr(request.user, 'is_admin', False)
        )


class ServiceViewSet(viewsets.ModelViewSet):
    """
    Government places directory.

    Reads are public. POST / PUT / PATCH / DELETE require an admin token
    and accept the full nested payload (phones + hours) in one request.

    List query params: category, district, emergency=true, search
    (search matches name / department / address in all three languages).
    """

    serializer_class = ServiceSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        queryset = Service.objects.prefetch_related('phones').select_related('hours')
        params = self.request.query_params

        category = params.get('category')
        district = params.get('district')
        emergency = params.get('emergency')
        search = params.get('search')

        if category:
            queryset = queryset.filter(category=category)
        if district:
            queryset = queryset.filter(district__iexact=district)
        if emergency is not None:
            queryset = queryset.filter(is_emergency=emergency.lower() in ('1', 'true', 'yes'))
        if search:
            queryset = queryset.filter(
                Q(name_en__icontains=search) | Q(name_si__icontains=search)
                | Q(name_ta__icontains=search)
                | Q(department_en__icontains=search) | Q(department_si__icontains=search)
                | Q(department_ta__icontains=search)
                | Q(address_en__icontains=search) | Q(address_si__icontains=search)
                | Q(address_ta__icontains=search)
            )
        return queryset

    @action(detail=False, methods=['get'])
    def districts(self, request):
        districts = (
            Service.objects.order_by('district')
            .values_list('district', flat=True)
            .distinct()
        )
        return Response(list(districts))

    @action(detail=False, methods=['get'])
    def categories(self, request):
        return Response([
            {'id': value, 'label': label} for value, label in ServiceCategory.choices
        ])
