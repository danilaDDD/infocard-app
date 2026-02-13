from django.db import models

# Create your models here.
class AbsCreated(models.Model):
    """
    Модель, помогающая отследить дату создания и изменения объекта.
    """

    updated = models.DateTimeField('Дата изменения', auto_now=True)
    created = models.DateTimeField('Дата создания', auto_now_add=True)

    class Meta:
        abstract = True

class AbsActive(models.Model):
    is_active = models.BooleanField('Статус активности', default=True)

    class Meta:
        abstract = True