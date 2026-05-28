from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils.timezone import now
from netfields import CidrAddressField


class System(models.Model):
    ci = models.CharField(verbose_name='CI', unique=True)
    name = models.CharField(verbose_name='Имя')
    is_it_service = models.BooleanField(verbose_name='IT-Услуга?')
    is_active = models.BooleanField(verbose_name='Активена?')

    created_at = models.DateTimeField(verbose_name='Время создания', default=now)
    updated_at = models.DateTimeField(verbose_name='Время последнего обновления', auto_now=True)


class Stand(models.Model):
    ci = models.CharField(verbose_name='CI', unique=True)
    has_anonymized_data = models.BooleanField(verbose_name='Содержит обезличенные данные?')
    ips = ArrayField(CidrAddressField(verbose_name='IP-адреса'), default=list)
    is_active = models.BooleanField(verbose_name='Активен?')
    name = models.CharField(verbose_name='Имя')

    system = models.ForeignKey(
        System,
        on_delete=models.PROTECT,
        related_name='stands',
        verbose_name='Система',
    )

    created_at = models.DateTimeField(verbose_name='Время создания', default=now)
    updated_at = models.DateTimeField(verbose_name='Время последнего обновления', auto_now=True)
