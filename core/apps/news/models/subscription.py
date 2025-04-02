from django.db import models

from core.apps.common.models import (
    TimedBaseModel,
)
from core.apps.news.models.faculty import Faculty
from core.apps.news.models.tag import Tag
from core.apps.news.models.user import User
from core.apps.news.entities.subscription import Subscription as SubscriptionEntity

class Subscription(TimedBaseModel):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_subscriptions',
    )
    faculties = models.ManyToManyField(
        Faculty,
        related_name='faculties_subscriptions',
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='tags_subscriptions',
    )

    def to_entity(self) -> SubscriptionEntity:
        return SubscriptionEntity(
            id=self.id,
            faculties=[Faculty(faculty.id) for faculty in self.faculties.all()],
            tags=[Tag(tag.id) for tag in self.tags.all()],
            created_at=self.created_at,
            updated_at=self.updated_at,
        )

    def __str__(self):
        return (
            f"{self.user.last_name}\n"
        )

    class Meta:
        verbose_name = "Subscription"
        verbose_name_plural = "Subscriptions"