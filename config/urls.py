"""URL configuration for the LankaSeva backend."""
from django.urls import include, path

urlpatterns = [
    path('api/auth/', include('accounts.urls')),
    path('api/services/', include('services.urls')),
    path('api/reviews/', include('reviews.urls')),
    path('api/emergency/', include('emergency.urls')),
]
