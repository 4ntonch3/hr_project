import uuid

from django.db import models
from django.utils.timezone import now

from apps.users.models import User

from .access_group import AccessGroup
from .network_zone import NetworkZone


class NetworkInteractionSource(models.Model):
    src_network_zone = models.ForeignKey(
        NetworkZone,
        on_delete=models.PROTECT,
        verbose_name="Сетевая Зона источника",
        related_name="network_interactions_where_src",
    )
    dst_network_zone = models.ForeignKey(
        NetworkZone,
        on_delete=models.PROTECT,
        verbose_name="Сетевая Зона назначения",
        related_name="network_interactions_where_dst",
    )

    arch_interaction_guid = models.CharField(
        verbose_name="ID сущности из архитектурного описания",
        max_length=128,
        unique=True,
    )
    creation_reason = models.TextField(verbose_name="Обоснование создания")
    protocol_to_ports = models.TextField(
        verbose_name="Связь протоколов и портов",
        help_text='{"TCP":["43","443"],"UDP":["444"]}',
    )
    unactual_at = models.DateTimeField(
        verbose_name="Дата потери актуальности", blank=True, null=True
    )
    unactuality_reason = models.TextField(
        verbose_name="Обоснование потери актуальности", blank=True, null=True
    )
    created_at = models.DateTimeField(verbose_name="Время создания", default=now)
    updated_at = models.DateTimeField(
        verbose_name="Время последнего обновления", auto_now=True
    )

    class Meta:
        verbose_name = "Источник Сетевого Взаимодействия"
        verbose_name_plural = "Источники Сетевого Взаимодействия"


class NetworkInteraction(models.Model):
    source = models.OneToOneField(
        NetworkInteractionSource,
        on_delete=models.PROTECT,
        verbose_name="Источник",
        related_name="network_interaction",
    )
    src_access_group = models.ForeignKey(
        AccessGroup,
        on_delete=models.PROTECT,
        verbose_name="Группа Доступа источника",
        related_name="network_interactions_where_src",
    )
    dst_access_group = models.ForeignKey(
        AccessGroup,
        on_delete=models.PROTECT,
        verbose_name="Группа Доступа назначения",
        related_name="network_interactions_where_dst",
    )
    activity_initiator = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        verbose_name="Пользователь, активировавшие Сетевое Взаимодействие",
        blank=True,
        null=True,
    )

    public_id = models.CharField(
        verbose_name="Публичный ID",
        max_length=128,
        default=uuid.uuid4,
        unique=True,
    )
    creation_reason = models.TextField(verbose_name="Обоснование создания")
    activated_at = models.DateTimeField(
        verbose_name="Время активации", blank=True, null=True
    )
    created_at = models.DateTimeField(verbose_name="Время создания", default=now)
    updated_at = models.DateTimeField(
        verbose_name="Время последнего обновления", auto_now=True
    )

    class Meta:
        verbose_name = "Сетевое Взаимодействие"
        verbose_name_plural = "Сетевые Взаимодействия"
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "src_access_group",
                    "dst_access_group",
                    "source",
                ],
                name="%(app_label)s_%(class)s_unique_network_interaction",
            )
        ]
