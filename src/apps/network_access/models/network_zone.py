from django.db import models
from django.utils.timezone import now


class NetworkZone(models.Model):
    public_id = models.CharField(verbose_name='Публичный ID', max_length=128, unique=True)
    name = models.CharField(verbose_name='Название', max_length=256, unique=True)
    creation_reason = models.TextField(verbose_name='Обоснование создания')
    created_at = models.DateTimeField(verbose_name='Время создания', default=now)
    updated_at = models.DateTimeField(verbose_name='Время последнего обновления', auto_now=True)
