from django.core.management import BaseCommand

from apps.account.models import PrimaryToken


class Command(BaseCommand):
    help = 'Create primary token'

    def handle(self, *args, **options):
        title = input('Введите название токена: ')
        token = input('Введите токен: ')

        PrimaryToken.objects.create(token=token, title=title, is_active=True)
