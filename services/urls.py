from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ServiceViewSet, CategoryViewSet

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'', ServiceViewSet, basename='service')

urlpatterns = [
    path('', include(router.urls)),
]
