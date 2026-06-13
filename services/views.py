from django.db.models import Q
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from config.permissions import IsAdminOrReadOnly

from .models import Service, Category
from .serializers import ServiceSerializer, CategorySerializer

class CategoryViewSet(viewsets.ModelViewSet):
    """
    CRUD for categories.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]

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
        queryset = (Service.objects.select_related('hours', 'category')
                    .prefetch_related('phones', 'hours__slots'))
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
            {'id': c.code, 'label': c.name_en} for c in Category.objects.all()
        ])
