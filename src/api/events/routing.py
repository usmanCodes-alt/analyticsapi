from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select

# from timescaledb.utils import get_utc_now
from timescaledb.hyperfunctions import time_bucket
from sqlalchemy import func, case

from api.db.session import get_session
from .models import (
    EventModel,
    EventBucketSchema,
    EventCreateSchema,
    # EventUpdateSchema,
)


router = APIRouter()

DEFAULT_LOOKUP_PAGES = [
    "/",
    "/about",
    "/pricing",
    "/contact",
    "/blog",
    "/products",
    "/login",
    "/signup",
    "/dashboard",
    "/settings",
]


@router.get("/", response_model=List[EventBucketSchema])
def read_events(
    duration: str = Query(default="1 day"),
    pages: List = Query(default=None),
    session: Session = Depends(get_session),
):
    os_case = case(
        (EventModel.user_agent.ilike("%windows%"), "Windows"),
        (EventModel.user_agent.ilike("%macintosh%"), "MacOS"),
        (EventModel.user_agent.ilike("%iphone%"), "iOS"),
        (EventModel.user_agent.ilike("%android%"), "Android"),
        (EventModel.user_agent.ilike("%linux%"), "Linux"),
        else_="Other",
    ).label("operating_system")
    bucket = time_bucket(duration, EventModel.time)
    pages = (
        pages if isinstance(pages, list) and len(pages) > 0 else DEFAULT_LOOKUP_PAGES
    )
    query = (
        select(
            bucket.label("bucket"),
            os_case,
            EventModel.page.label("page"),
            func.avg(EventModel.duration).label("avg_duration"),
            func.count().label("event_count"),
        )
        .where(
            EventModel.page.in_(pages),
        )
        .group_by(bucket, EventModel.page, os_case)
        .order_by(bucket, EventModel.page, os_case)
    )
    results = session.exec(query).fetchall()
    print(results)
    return results


@router.get("/{event_id}", response_model=EventModel)
def read_event(event_id: int, session: Session = Depends(get_session)):
    query = select(EventModel).where(EventModel.id == event_id)
    result = session.exec(query).first()
    if not result:
        raise HTTPException(status_code=404, detail="Event not found!")
    return result


@router.post("/", response_model=EventModel)
def create_event(payload: EventCreateSchema, session: Session = Depends(get_session)):
    data = payload.model_dump()
    instance = EventModel.model_validate(data)
    session.add(instance=instance)
    session.commit()
    session.refresh(instance=instance)
    return instance
