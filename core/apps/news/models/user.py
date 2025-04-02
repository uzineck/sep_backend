from django.db import models

from core.apps.common.models import (
    UserRole,
    TimedBaseModel,
)
from core.apps.news.entities.user import User as UserEntity

class User(TimedBaseModel):
    first_name = models.CharField(
        verbose_name="User's First Name",
        max_length=100,
    )
    last_name = models.CharField(
        verbose_name="User's Last name",
        max_length=100,
    )
    middle_name = models.CharField(
        verbose_name="User's Middle Name",
        max_length=100,
    )
    role = models.CharField(
        choices=UserRole,
        verbose_name="User's Roles",
    )
    score = models.FloatField(
        verbose_name="User's Score",
    )
    email = models.EmailField(
        verbose_name="User's email for auth",
        max_length=255,
        unique=True,
        blank=False,
    )
    password = models.CharField(
        max_length=250,
        blank=False,
        null=False,
    )

    def to_entity(self) -> UserEntity:
        return UserEntity(
            id=self.id,
            first_name=self.first_name,
            last_name=self.last_name,
            role=UserRole(self.role),
            email=self.email,
            score=self.score,
            password=self.password,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )

    def __str__(self):
        return f"{self.last_name} {self.first_name[0]}."

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        indexes = [
            models.Index(fields=["email"]),
        ]
