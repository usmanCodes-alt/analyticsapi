from contextlib import asynccontextmanager
from fastapi import FastAPI

from api.db.session import init_db
from api.events import router as event_rounter


@asynccontextmanager
async def lifespan(app: FastAPI):
    # before app start up
    init_db()
    yield
    # clean up


app = FastAPI(lifespan=lifespan)
app.include_router(event_rounter, prefix="/api/events")


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/healthz")
def read_api_health():
    return {"status": "ok"}
