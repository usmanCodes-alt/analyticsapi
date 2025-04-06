from fastapi import APIRouter
from .models import EventModel, EventListSchema, EventCreateSchema, EventUpdateSchema
from ..db.config import DATABASE_URL

router = APIRouter()


@router.get("/")
def read_events() -> EventListSchema:
    print('Database URL from env: ', DATABASE_URL)
    return {"results": [{"id": 1}, {"id": 2}, {"id": 3}], "count": 3}


@router.get("/{event_id}")
def read_event(event_id: int) -> EventModel:
    return {"id": event_id}


@router.post("/")
def create_event(payload: EventCreateSchema) -> EventModel:
    # print(payload.page)
    data = payload.model_dump()
    return {"id": 123, **data}


@router.put("/{event_id}")
def put_event(event_id: int, payload: EventUpdateSchema) -> EventModel:
    # print(event_id, payload.description)
    data = payload.model_dump()
    return {"id": 123, **data}
