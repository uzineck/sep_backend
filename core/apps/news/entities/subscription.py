from dataclasses import (
    dataclass,
    field,
)
from datetime import datetime

from core.apps.news.entities.faculty import Faculty
from core.apps.news.entities.tag import Tag
from core.apps.news.entities.user import User


@dataclass
class Subscription:
    id: int | None = field(default=None, kw_only=True) # noqa
    user: User | None = field(default=None, kw_only=True)
    tags: list[Tag] | None = field(default=None, kw_only=True)
    faculties: list[Faculty] | None = field(default=None, kw_only=True)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime | None = field(default=None)
