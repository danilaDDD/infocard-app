from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from drf_spectacular.utils import extend_schema

from apps.account.permissions import PrimaryTokenPermission
from apps.account.serializers import AccountRegistrationSerializer, AccountSerializer, \
    AccountRegistrationResponseSerializer


# Create your views here.
class RegistrationAPIView(APIView):
    serializer_class = AccountRegistrationSerializer
    permission_classes = [PrimaryTokenPermission]

    @extend_schema(
        tags=['account'],
        summary='Регистрация нового пользователя',
        description='Регистрация нового пользователя с проверкой регистрационного токена',
        request=AccountRegistrationSerializer,
        responses={
            201: AccountRegistrationResponseSerializer,
        }
    )
    def post(self, request: Request):
        serializer = self.serializer_class(data=request.data)

        serializer.is_valid(raise_exception=True)
        account = serializer.save()

        resp_data = AccountRegistrationResponseSerializer(account).data
        return Response(resp_data, status=status.HTTP_201_CREATED)


