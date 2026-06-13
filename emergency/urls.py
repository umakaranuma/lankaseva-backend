from django.urls import path

from .views import EmergencyHotlineList

urlpatterns = [
    path('', EmergencyHotlineList.as_view(), name='emergency-hotlines'),
]
