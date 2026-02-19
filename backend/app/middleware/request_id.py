import uuid

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

from app.middleware.request_context import set_request_id


class RequestIdMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = request.headers.get("x-request-id") or str(uuid.uuid4())
        set_request_id(request_id)
        response = await call_next(request)
        response.headers["x-request-id"] = request_id
        return response
