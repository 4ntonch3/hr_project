import uuid

from django.db import models
from django.utils.timezone import now

from apps.network_access.models.network_zone import NetworkZone
from apps.network_access.models.prefix import Prefix
from apps.users.models import User


class AccessGroupSource(models.Model):
    public_id = models.CharField(verbose_name='Публичный ID', max_length=128, unique=True)
    network_zones = models.ManyToManyField(
        NetworkZone,
        verbose_name='Сетевые зоны',
        related_name='access_groups',
    )

    arch_stand_guid = models.CharField(verbose_name='ID Стенда из архитектурного описания', max_length=128)
    arch_component_guid = models.CharField(verbose_name='ID Компонента из архитектурного описания', max_length=128)
    unactual_at = models.DateTimeField(verbose_name='Время потери актуальности', blank=True, null=True)
    unactuality_reason = models.TextField(verbose_name='Обоснование потери актуальности', blank=True, null=True)
    creation_reason = models.TextField(verbose_name='Обоснование создания')
    created_at = models.DateTimeField(verbose_name='Время создания', default=now)
    updated_at = models.DateTimeField(verbose_name='Время последнего обновления', auto_now=True)

    class Meta:
        verbose_name = 'Источник Группы Доступа'
        verbose_name_plural = 'Источники Групп Доступа'


class AccessGroup(models.Model):
    source = models.OneToOneField(
        AccessGroupSource,
        on_delete=models.PROTECT,
        verbose_name='Источник',
    )

    public_id = models.CharField(
        verbose_name='Публичный ID',
        max_length=128,
        default=uuid.uuid4,
        unique=True,
    )
    name = models.TextField(verbose_name='Название')
    created_at = models.DateTimeField(verbose_name='Время создания', default=now)
    updated_at = models.DateTimeField(verbose_name='Время последнего обновления', auto_now=True)

    class Meta:
        verbose_name = 'Группа Доступа'
        verbose_name_plural = 'Группы Доступа'


class AccessGroup2Prefix(models.Model):
    public_id = models.CharField(verbose_name='Публичный ID', max_length=128, unique=True)
    access_group = models.ForeignKey(
        AccessGroup,
        on_delete=models.CASCADE,
        verbose_name='Группа Доступа',
    )
    prefix = models.ForeignKey(
        Prefix,
        on_delete=models.CASCADE,
        verbose_name='Префикс',
    )
    approver = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        verbose_name='Администратор, утвердивший связь',
        blank=True,
        null=True,
    )

    approved_at = models.DateTimeField(
        verbose_name='Время утверждения',
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(verbose_name='Время создания', default=now)
    updated_at = models.DateTimeField(verbose_name='Время последнего обновления', auto_now=True)

    class Meta:
        verbose_name = 'Связь Группы Доступа и Префикса'
        verbose_name_plural = 'Связь Групп Доступа и Префиксов'
        constraints = [
            models.UniqueConstraint(
                fields=['access_group', 'prefix'],
                name='%(app_label)s_%(class)s_unique_access_group_to_prefix',
            )
        ]
