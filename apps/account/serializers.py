from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from apps.account.models import Account


class AccountRegistrationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True, allow_blank=False, min_length=3)
    first_name = serializers.CharField(required=True, allow_blank=False, min_length=3)
    last_name = serializers.CharField(required=True, allow_blank=False, min_length=3)
    email = serializers.EmailField(required=True, allow_blank=False, min_length=3)
    phone = serializers.CharField(required=True, allow_blank=False, min_length=3, max_length=15)
    password = serializers.CharField(write_only=True, required=True, allow_blank=False, min_length=6)
    birth_date = serializers.DateField(required=True, allow_null=True)

    class Meta:
        model = Account
        fields = ('username', 'first_name', 'last_name', 'patronymic',
                  'email', 'phone',  'password', 'birth_date',
                  'gender', 'telegram_id', )

    def create(self, validated_data):
        password = validated_data.pop('password')
        account = Account(**validated_data)
        account.set_password(password)
        account.save()
        return account


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, allow_blank=False, min_length=3)
    password = serializers.CharField(write_only=True, required=True, allow_blank=False, min_length=6)


class RefreshTokenSerializer(serializers.Serializer):
    refresh = serializers.CharField(required=True, allow_blank=False, min_length=6)


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('id', 'username', 'first_name', 'last_name', 'patronymic',
                  'email', 'phone',  'birth_date', 'gender', 'telegram_id', )


class TokensSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    access = serializers.CharField()


class AccountRegistrationResponseSerializer(serializers.Serializer):
    user = AccountSerializer()
    tokens = TokensSerializer()

    def to_representation(self, instance: Account):
        user_data = AccountSerializer(instance).data

        refresh = RefreshToken.for_user(instance)
        tokens_data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

        return {
            'user': user_data,
            'tokens': tokens_data,
        }


class AuthResponseSerializer(serializers.Serializer):
    access = serializers.CharField(required=True, allow_blank=False)
    refresh = serializers.CharField(required=True, allow_blank=False)

    def to_representation(self, instance: Account):
        refresh = RefreshToken.for_user(instance)
        tokens_data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

        return tokens_data
