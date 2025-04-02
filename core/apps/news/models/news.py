from django.db import models

from core.apps.common.models import (
    TimedBaseModel,
)
from core.apps.news.models.faculty import Faculty
from core.apps.news.models.tag import Tag
from core.apps.news.models.user import User
from core.apps.news.entities.news import News as NewsEntity

class News(TimedBaseModel):
    title = models.CharField(
        max_length=150,
        verbose_name='News name',
    )
    description = models.TextField(
        verbose_name='News description',
    )
    content = models.TextField(
        verbose_name='News content',
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_news',
        verbose_name='News user',
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='News tags',
        related_name='news_tags',
    )
    faculty = models.ForeignKey(
        Faculty,
        on_delete=models.CASCADE,
        related_name='news_faculty',
        verbose_name='News faculty',
        blank=True,
        null=True,
    )

    def to_entity(self) -> NewsEntity:
        return NewsEntity(
            id=self.id,
            title=self.title,
            description=self.description,
            content=self.content,
            user=self.user,
            tags=[Tag(tag.id) for tag in self.tags.all()],
            faculty=self.faculty,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )

    def __str__(self):
        return (
            f"{self.title}\n"
        )

    class Meta:
        verbose_name = "News"
        verbose_name_plural = "News"