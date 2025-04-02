from dataclasses import (
    dataclass,
    field,
)
from datetime import datetime


@dataclass
class Tag:
    id: int | None = field(default=None, kw_only=True) # noqa
    name: str | None = field(default=None, kw_only=True)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime | None = field(default=None)
