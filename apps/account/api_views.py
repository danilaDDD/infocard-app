from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from drf_spectacular.utils import extend_schema

from apps.account.models import Account
from apps.account.permissions import PrimaryTokenPermission
from apps.account.serializers import AccountRegistrationSerializer, AccountSerializer, \
    AccountRegistrationResponseSerializer, LoginSerializer, AuthResponseSerializer


# Create your views here.
class AuthAPIView(APIView):
    permission_classes = [PrimaryTokenPermission]


class RegistrationAPIView(AuthAPIView):
    serializer_class = AccountRegistrationSerializer

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


class LoginAPIView(AuthAPIView):
    serializer_class = LoginSerializer

    @extend_schema(
        tags=['account'],
        summary='Авторизация пользователя',
        description='Авторизация пользователя с проверкой регистрационного токена',
        request=LoginSerializer,
        responses={
            200: AuthResponseSerializer,
        }
    )
    def post(self, request: Request):
        serializer = self.serializer_class(data=request.data)

        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get('username')
        password = serializer.validated_data.get('password')

        account = Account.objects.filter(username=username).first()

        if account is None or not account.check_password(password):
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        resp_data = AuthResponseSerializer(instance=account).data
        return Response(resp_data, status=status.HTTP_200_OK)


