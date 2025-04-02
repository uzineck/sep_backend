from django.db import models

from core.apps.common.models import (
    TimedBaseModel,
)
from core.apps.news.entities.faculty import Faculty as FacultyEntity


class Faculty(TimedBaseModel):
    name = models.CharField(
        verbose_name='Faculty name',
        max_length=100,
    )

    def to_entity(self) -> FacultyEntity:
        return FacultyEntity(
            id=self.id,
            name=self.name,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )

    def __str__(self):
        return (
            f"{self.name}\n"
        )

    class Meta:
        verbose_name = "Faculty"
        verbose_name_plural = "Faculties"