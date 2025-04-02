from django.db import models


class TimedBaseModel(models.Model):
    created_at = models.DateTimeField(
        verbose_name='Created date',
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        verbose_name='Updated date',
        auto_now=True,
    )

    class Meta:
        abstract = True


class UserRole(models.TextChoices):
    ADMIN = "admin", "Admin"
    MANAGER = "manager", "Manager"
    CREATOR = "creator", "Creator"


class TokenType(models.TextChoices):
    ACCESS = "access", "ACCESS"
    REFRESH = "refresh", "REFRESH"
