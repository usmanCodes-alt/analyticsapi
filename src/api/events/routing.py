from fastapi import APIRouter
from .schemas import EventSchema, EventListSchema

router = APIRouter()


@router.get("/")
def read_events() -> EventListSchema:
    return {"results": [{"id": 1}, {"id": 2}, {"id": 3}], "count": 3}


@router.get("/{event_id}")
def read_event(event_id: int) -> EventSchema:
    return {"id": event_id}


@router.post("/")
def create_event(data: dict = {}) -> EventSchema:
    print(data)
    return {"id": 123}


@router.put("/{event_id}")
def create_event(event_id: int, data: dict = {}) -> EventSchema:
    print(data)
    return {"id": 123}
