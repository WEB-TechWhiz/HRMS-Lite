from contextvars import ContextVar

request_id_ctx: ContextVar[str | None] = ContextVar("request_id", default=None)


def set_request_id(request_id: str):
    request_id_ctx.set(request_id)


def get_request_id() -> str | None:
    return request_id_ctx.get()
