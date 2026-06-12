from django.urls import path

from .views import DeleteAccountView, LogoutView, ProfileView, SendOTPView, VerifyOTPView

urlpatterns = [
    path('otp/send/', SendOTPView.as_view(), name='send-otp'),
    path('otp/verify/', VerifyOTPView.as_view(), name='verify-otp'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('account/', DeleteAccountView.as_view(), name='delete-account'),
]
