from django.db import models
from netfields import CidrAddressField, NetManager

from .network_zone import NetworkZone


class Prefix(models.Model):
    network_zone = models.ForeignKey(
        NetworkZone,
        on_delete=models.PROTECT,
        verbose_name="Сетевая Зона",
    )

    address = CidrAddressField(verbose_name="Префикс")

    objects = NetManager()

    class Meta:
        verbose_name = "Префикс"
        verbose_name_plural = "Префиксы"
