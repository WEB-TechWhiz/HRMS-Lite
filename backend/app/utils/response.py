def success_response(data=None, message="Success", meta=None):
    return {
        "success": True,
        "message": message,
        "data": data,
        "meta": meta,
    }


def error_response(message: str, code: str, details=None, meta=None):
    return {
        "success": False,
        "message": message,
        "error": {
            "code": code,
            "details": details,
        },
        "meta": meta,
    }
