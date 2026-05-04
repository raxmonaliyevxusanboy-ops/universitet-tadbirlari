from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

from app.config import engine, Base
from app.models.user import User
from app.models.venue import Venue
from app.models.event import EventSchedule

from app.routers.users import router as users_router
from app.routers.venues import router as venues_router
from app.routers.events import router as events_router

# Jadvallarni yaratish
Base.metadata.create_all(bind=engine)

app = FastAPI(title="University Event Scheduler")

# CORS sozlamalari (Brauzer xatolarini oldini olish uchun)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routerlarni ulash
app.include_router(users_router, prefix="/users", tags=["Users"])
app.include_router(venues_router, prefix="/venues", tags=["Venues"])
app.include_router(events_router, prefix="/events", tags=["Events"])

# Static fayllar
app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/")
def home():
    return FileResponse("app/static/index.html")