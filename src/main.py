from typing import Union
from fastapi import FastAPI

from api.events import router as event_rounter

app = FastAPI()
app.include_router(event_rounter, prefix="/api/events")


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/healthz")
def read_api_health():
    return {"status": "ok"}
