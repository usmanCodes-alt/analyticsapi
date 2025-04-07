from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from api.db.session import get_session
from .models import (
    EventModel,
    EventListSchema,
    EventCreateSchema,
    EventUpdateSchema,
    get_utc_now,
)


router = APIRouter()


@router.get("/", response_model=EventListSchema)
def read_events(session: Session = Depends(get_session)):
    query = select(EventModel).order_by(EventModel.id.desc()).limit(10)
    result = session.exec(query).all()
    return {"results": result, "count": len(result)}


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
