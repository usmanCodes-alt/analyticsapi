from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
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
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(event_rounter, prefix="/api/events")


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/healthz")
def read_api_health():
    return {"status": "ok"}
