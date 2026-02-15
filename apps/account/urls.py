from django.urls import path

from apps.account.api_views import RegistrationAPIView

app_name = 'account'

urlpatterns = [
    path('', RegistrationAPIView.as_view(), name='add_user'),
]