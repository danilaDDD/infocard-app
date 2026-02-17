from django.urls import path

from apps.account.api_views import RegistrationAPIView, LoginAPIView, RefreshTokenAPIView

app_name = 'account'

urlpatterns = [
    path('', RegistrationAPIView.as_view(), name='add_user'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('refresh/', RefreshTokenAPIView.as_view(), name='refresh_token'),
]