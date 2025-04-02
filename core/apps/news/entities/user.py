from dataclasses import (
    dataclass,
    field,
)
from datetime import datetime

from core.apps.common.models import UserRole


@dataclass
class User:
    id: int | None = field(default=None, kw_only=True) # noqa
    first_name: str | None = field(default=None, kw_only=True)
    last_name: str | None = field(default=None, kw_only=True)
    email: str | None = field(default=None, kw_only=True)
    role: UserRole | None = field(default=None, kw_only=True)
    password: str | None = field(default=None, kw_only=True)
    score: float | None = field(default=None, kw_only=True)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime | None = field(default=None)
