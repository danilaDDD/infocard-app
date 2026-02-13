from django.contrib.auth.models import UserManager, AbstractUser
from django.db import models

from apps.common.models import AbsCreated, AbsActive


# Create your models here.
class PrimaryToken(AbsCreated, AbsActive):
    title = models.CharField('Название', max_length=255)
    token = models.CharField('Токен', max_length=255)

class Account(AbsCreated, AbstractUser):
    NONE_GENDER = 'none'
    MALE_GENDER = 'male'
    FEMALE_GENDER = 'female'
    GENDERS = (
        (NONE_GENDER, 'Не указан'),
        (MALE_GENDER, 'Мужской'),
        (FEMALE_GENDER, 'Женский')
    )

    phone = models.CharField('Номер телефона', max_length=50, blank=True)
    birth_date = models.DateField('Дата рождения', null=True, blank=True)
    gender = models.CharField('Пол', max_length=20, choices=GENDERS, default=NONE_GENDER)
    patronymic = models.CharField('Отчество', max_length=50, blank=True)
    telegram_id = models.BigIntegerField('Telegram ID', null=True, blank=True)

    objects = UserManager()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'