from django.db import models

from core.apps.common.models import (
    TimedBaseModel,
)
from core.apps.news.models.news import News
from core.apps.news.models.user import User
from core.apps.news.entities.comment import Comment as CommentEntity

class Comment(TimedBaseModel):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_comments',
        verbose_name='Comment user',
    )
    text = models.TextField(verbose_name='Comment text')
    news = models.ForeignKey(
        News,
        on_delete=models.CASCADE,
        related_name='news_comments',
        verbose_name='Comment news',
    )
    def to_entity(self) -> CommentEntity:
        return CommentEntity(
            id=self.id,
            text=self.text,
            user=self.user,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )

    def __str__(self):
        return (
            f"{self.user.last_name} {self.news.title}"
        )

    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"