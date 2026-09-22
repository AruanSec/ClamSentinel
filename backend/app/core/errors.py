from fastapi import HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


def error_response(code: str, message: str, status_code: int) -> JSONResponse:
    return JSONResponse(status_code=status_code, content={"error": {"code": code, "message": message}})


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    del request
    detail = exc.detail if isinstance(exc.detail, str) else "Request failed"
    return error_response(f"HTTP_{exc.status_code}", detail, exc.status_code)


async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    del request
    del exc
    return error_response("VALIDATION_ERROR", "Request validation failed", status.HTTP_422_UNPROCESSABLE_ENTITY)


async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    del request
    del exc
    return error_response("INTERNAL_SERVER_ERROR", "An internal server error occurred", status.HTTP_500_INTERNAL_SERVER_ERROR)