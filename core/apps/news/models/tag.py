from django.db import models

from core.apps.common.models import (
    TimedBaseModel,
)
from core.apps.news.entities.tag import Tag as TagEntity


class Tag(TimedBaseModel):
    
    name = models.CharField(
        verbose_name='Tag name',
        max_length=100,
    )

    def to_entity(self) -> TagEntity:
        return TagEntity(
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
        verbose_name = "Tag"
        verbose_name_plural = "Tags"