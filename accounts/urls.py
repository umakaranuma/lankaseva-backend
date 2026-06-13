from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import DeleteAccountView, LogoutView, ProfileView, SendOTPView, VerifyOTPView, AdminUserViewSet, AdminLoginView

router = DefaultRouter()
router.register(r'admin/users', AdminUserViewSet, basename='admin-user')

urlpatterns = [
    path('otp/send/', SendOTPView.as_view(), name='send-otp'),
    path('otp/verify/', VerifyOTPView.as_view(), name='verify-otp'),
    path('admin/login/', AdminLoginView.as_view(), name='admin_login'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('account/', DeleteAccountView.as_view(), name='delete-account'),
    path('', include(router.urls)),
]
