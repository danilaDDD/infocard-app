from django.urls import path

from apps.account.api_views import RegistrationAPIView, LoginAPIView

app_name = 'account'

urlpatterns = [
    path('', RegistrationAPIView.as_view(), name='add_user'),
    path('login/', LoginAPIView.as_view(), name='login'),
]