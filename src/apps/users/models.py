from django.contrib.auth.models import AbstractUser
from django.db import models


class Department(models.Model):
    name = models.CharField(max_length=256)
    slug = models.CharField(max_length=3)

    class Meta:
        verbose_name = "Департамент"
        verbose_name_plural = "Департаменты"


class User(AbstractUser):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True)
