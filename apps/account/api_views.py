from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from drf_spectacular.utils import extend_schema

from apps.account.models import Account
from apps.account.permissions import PrimaryTokenPermission
from apps.account.serializers import AccountRegistrationSerializer, \
    AccountRegistrationResponseSerializer, LoginSerializer, AuthResponseSerializer, RefreshTokenSerializer


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


class RefreshTokenAPIView(AuthAPIView):
    serializer_class = RefreshTokenSerializer

    @extend_schema(
        tags=['account'],
        summary='Обновление access токена',
        description='Обновление access токена с помощью refresh токена и проверкой регистрационного токена',
        responses={
            200: AuthResponseSerializer,
        }
    )
    def post(self, request: Request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        refresh_token = serializer.validated_data.get('refresh')

        try:
            decoded_obj = RefreshToken(refresh_token)
        except TokenError as e:
            return Response({'detail': 'Invalid refresh token'}, status=status.HTTP_401_UNAUTHORIZED)

        account_id = int(decoded_obj["user_id"])
        account = Account.objects.filter(id=account_id).first()

        if account is None:
            return Response({'detail': 'Invalid refresh token'}, status=status.HTTP_401_UNAUTHORIZED)

        resp_data = AuthResponseSerializer(instance=account).data
        return Response(resp_data, status=status.HTTP_200_OK)
