from django.db import models
from django.utils.timezone import now

from apps.elt.enum import ELTStatus, SystemType


class FullELTVersion(models.Model):
    status: ELTStatus = models.CharField(verbose_name='Статус')
    info = models.JSONField(verbose_name='Детали загрузки', null=True)

    created_at = models.DateTimeField(verbose_name='Время создания', default=now)
    updated_at = models.DateTimeField(verbose_name='Время последнего обновления', auto_now=True)

    class Meta:
        verbose_name = 'Версия выгрузки'
        verbose_name_plural = 'Версии выгрузок'


class ELTSystem(models.Model):
    ci = models.CharField(verbose_name='CI', null=False)
    system_type: SystemType = models.CharField(verbose_name='Тип системы', null=False)
    name = models.CharField(verbose_name='Имя', null=False)
    status = models.CharField(verbose_name='Статус', null=True)
    is_it_service = models.BooleanField(verbose_name='ИТ-Услуга?', null=True, blank=True)

    related_systems = models.ManyToManyField('self', verbose_name='Связанные системы')
    version = models.ForeignKey(
        FullELTVersion,
        verbose_name='Версия',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(verbose_name='Время создания', default=now)
    updated_at = models.DateTimeField(verbose_name='Время последнего обновления', auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['ci', 'version'],
                name='unique_system_for_version',
            ),
        ]


class ELTStand(models.Model):
    ci = models.CharField(verbose_name='CI', null=False)
    sb_security_group = models.CharField(  # `t` == deanonymized
        verbose_name='Признак обезличенных данных', null=True, blank=True
    )
    status = models.CharField(verbose_name='Статус', null=True)
    name = models.CharField(verbose_name='Имя', null=True)
    subtype = models.CharField(verbose_name='Подтип', null=True, blank=True)
    devices = models.TextField(verbose_name='Связи с устройствами', null=True, blank=True)

    system = models.ForeignKey(ELTSystem, verbose_name='AC', on_delete=models.CASCADE, null=True, blank=True)
    version = models.ForeignKey(
        FullELTVersion,
        verbose_name='Версия',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(verbose_name='Время создания', default=now)
    updated_at = models.DateTimeField(verbose_name='Время последнего обновления', auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['ci', 'version'],
                name='unique_stand_for_version',
            ),
        ]


class ELTDevice(models.Model):
    type = models.CharField(verbose_name='Тип', null=True)
    subtype = models.CharField(verbose_name='Подтип', null=True)
    name = models.CharField(verbose_name='Имя', null=True)
    ci = models.CharField(verbose_name='CI', db_index=True)
    status = models.CharField(verbose_name='Статус', null=True)
    ips = models.TextField(  # separated by `;`
        verbose_name='Список IP-адресов', null=True, blank=True
    )

    version = models.ForeignKey(FullELTVersion, on_delete=models.CASCADE, verbose_name='Версия', null=True)

    created_at = models.DateTimeField(verbose_name='Время создания', default=now)
    updated_at = models.DateTimeField(verbose_name='Время последнего обновления', auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['ci', 'version'],
                name='unique_device_and_version',
            ),
        ]
