from datetime import datetime, timezone

from sqlmodel import SQLModel, Field

def utc_now():
    return datetime.now(timezone.utc)

class BaseSqlModel(SQLModel):
    create_at: datetime = Field(
        default_factory=utc_now,
        nullable=False
    )
