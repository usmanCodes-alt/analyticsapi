from datetime import datetime, timezone
from typing import List, Optional

# from pydantic import BaseModel, Field
import sqlmodel
from sqlmodel import SQLModel, Field


def get_utc_now():
    return datetime.now(timezone.utc).replace(tzinfo=timezone.utc)


class EventModel(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    page: Optional[str] = Field(default="")
    description: Optional[str] = Field(default="")
    created_at: datetime = Field(
        default_factory=get_utc_now,
        sa_type=sqlmodel.DateTime(timezone=True),
        nullable=False,
    )
    updated_at: datetime = Field(
        default_factory=get_utc_now,
        sa_type=sqlmodel.DateTime(timezone=True),
        nullable=False,
    )


class EventListSchema(SQLModel):
    results: List[EventModel]
    count: int


class EventCreateSchema(SQLModel):
    page: str
    description: Optional[str] = Field(default="")


class EventUpdateSchema(SQLModel):
    description: str
    page: Optional[str] = Field(default="")
