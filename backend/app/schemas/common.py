from typing import Any

from pydantic import BaseModel


class SuccessResponse(BaseModel):
    success: bool = True
    message: str
    data: Any = None
    meta: dict[str, Any] | None = None


class ErrorBody(BaseModel):
    code: str
    details: dict[str, Any] | None = None


class ErrorResponse(BaseModel):
    success: bool = False
    message: str
    error: ErrorBody
    meta: dict[str, Any] | None = None
