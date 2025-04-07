from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from timescaledb.utils import get_utc_now
from timescaledb.hyperfunctions import time_bucket
from sqlalchemy import func

from api.db.session import get_session
from .models import (
    EventModel,
    EventBucketSchema,
    EventCreateSchema,
    EventUpdateSchema,
)


router = APIRouter()

DEFAULT_LOOKUP_PAGES = ["/about", "/contact", "/pages", "/pricing", 'pricing']


@router.get("/", response_model=List[EventBucketSchema])
def read_events(
    duration: str = Query(default="1 day"),
    pages: List = Query(default=None),
    session: Session = Depends(get_session),
):
    bucket = time_bucket(duration, EventModel.time)
    pages = (
        pages if isinstance(pages, list) and len(pages) > 0 else DEFAULT_LOOKUP_PAGES
    )
    query = (
        select(
            bucket.label("bucket"),
            EventModel.page.label("page"),
            func.count().label("event_count"),
        )
        .where(EventModel.page.in_(pages))
        .group_by(bucket, EventModel.page)
        .order_by(bucket, EventModel.page)
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


@router.put("/{event_id}", response_model=EventModel)
def put_event(
    event_id: int, payload: EventUpdateSchema, session: Session = Depends(get_session)
):
    # print(event_id, payload.description)
    query = select(EventModel).where(EventModel.id == event_id)
    instance = session.exec(query).first()
    if not instance:
        raise HTTPException(status_code=404, detail="Event not found!")
    data = payload.model_dump()
    for k, v in data.items():
        # if k == 'id':
        #     continue
        setattr(instance, k, v)
    instance.updated_at = get_utc_now()
    session.add(instance=instance)
    session.commit()
    session.refresh(instance=instance)
    return instance
