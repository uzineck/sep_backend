from dataclasses import (
    dataclass,
    field,
)
from datetime import datetime

from core.apps.news.entities.news import News
from core.apps.news.entities.user import User


@dataclass
class Comment:
    id: int | None = field(default=None, kw_only=True) # noqa
    user: User | None = field(default=None, kw_only=True)
    text: str | None = field(default=None, kw_only=True)
    news: News | None = field(default=None, kw_only=True)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime | None = field(default=None)
