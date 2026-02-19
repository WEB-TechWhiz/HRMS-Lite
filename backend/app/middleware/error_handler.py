from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from app.core.constants import ErrorCode
from app.exceptions.custom_exceptions import AppException
from app.utils.response import error_response


def register_exception_handlers(app: FastAPI):
    @app.exception_handler(AppException)
    async def app_exception_handler(_: Request, exc: AppException):
        return JSONResponse(
            status_code=exc.status_code,
            content=error_response(message=exc.message, code=exc.code, details=exc.details),
        )

    @app.exception_handler(ValidationError)
    async def validation_exception_handler(_: Request, exc: ValidationError):
        return JSONResponse(
            status_code=400,
            content=error_response(
                message="Validation failed",
                code=ErrorCode.VALIDATION_ERROR,
                details={"errors": exc.errors()},
            ),
        )

    @app.exception_handler(Exception)
    async def generic_exception_handler(_: Request, exc: Exception):
        return JSONResponse(
            status_code=500,
            content=error_response(
                message="Internal server error",
                code=ErrorCode.SERVER_ERROR,
                details={"reason": str(exc)},
            ),
        )
