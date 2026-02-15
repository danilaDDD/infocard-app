from rest_framework import serializers

from apps.account.models import Account


class AccountRegistrationSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=True, allow_blank=False)
    last_name = serializers.CharField(required=True, allow_blank=False)
    email = serializers.EmailField(required=True, allow_blank=False)
    phone = serializers.CharField(required=True, allow_blank=False)
    password = serializers.CharField(write_only=True, required=True, allow_blank=False)
    birth_date = serializers.DateField(required=True, allow_null=True)

    class Meta:
        model = Account
        fields = ('first_name', 'last_name', 'patronymic',
                  'email', 'phone',  'password', 'birth_date',
                  'gender', 'telegram_id', )

    def create(self, validated_data):
        account = Account.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password']
        )
        return account

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('id', 'username', 'first_name', 'last_name', 'patronymic',
                  'email', 'phone',  'birth_date', 'gender', 'telegram_id', )