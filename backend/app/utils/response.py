from app.middleware.request_context import get_request_id


def success_response(data=None, message="Success", meta=None):
    default_meta = {"requestId": get_request_id()}
    if meta:
        default_meta.update(meta)

    return {
        "success": True,
        "message": message,
        "data": data,
        "meta": default_meta,
    }


def error_response(message: str, code: str, details=None, meta=None):
    default_meta = {"requestId": get_request_id()}
    if meta:
        default_meta.update(meta)

    return {
        "success": False,
        "message": message,
        "error": {
            "code": code,
            "details": details,
        },
        "meta": default_meta,
    }
