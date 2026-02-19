from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.attendance_routes import router as attendance_router
from app.api.employee_routes import router as employee_router
from app.core.config import settings
from app.database.base import Base
from app.database.connection import engine
from app.middleware.error_handler import register_exception_handlers

Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.app_name, version=settings.app_version)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

register_exception_handlers(app)

app.include_router(employee_router)
app.include_router(attendance_router)


@app.get("/health")
def health_check():
    return {"status": "ok"}
