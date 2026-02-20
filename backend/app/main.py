from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.attendance_routes import router as attendance_router
from app.api.employee_routes import router as employee_router
from app.core.config import settings
from app.database.connection import ensure_indexes, ping_database
from app.middleware.error_handler import register_exception_handlers
from app.middleware.request_id import RequestIdMiddleware
from app.utils.response import success_response


@asynccontextmanager
async def lifespan(_: FastAPI):
    ping_database()
    ensure_indexes()
    yield


app = FastAPI(title=settings.app_name, version=settings.app_version, lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(RequestIdMiddleware)

register_exception_handlers(app)

app.include_router(employee_router, prefix=settings.api_v1_prefix)
app.include_router(attendance_router, prefix=settings.api_v1_prefix)


@app.get("/")
def root():
    return success_response(
        data={"service": settings.app_name, "version": settings.app_version, "health": "/health"},
        message="HRMS Lite API running",
    )


@app.get("/health")
def health_check():
    return success_response(data={"status": "ok"}, message="Service healthy")
