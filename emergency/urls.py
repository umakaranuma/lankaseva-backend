from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import EmergencyHotlineViewSet

router = DefaultRouter()
router.register(r'', EmergencyHotlineViewSet, basename='emergency')

urlpatterns = [
    path('', include(router.urls)),
]
