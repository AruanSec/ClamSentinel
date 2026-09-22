import json
import logging
import time
import uuid

from fastapi import Request
from opentelemetry import trace
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import Response

from app.telemetry.metrics import REQUEST_COUNT, REQUEST_DURATION

logger = logging.getLogger("clamsentinel.http")


class RequestTelemetryMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        started_at = time.perf_counter()
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        span = trace.get_current_span()
        span.set_attribute("http.request_id", request_id)

        try:
            response = await call_next(request)
        except Exception:
            duration = time.perf_counter() - started_at
            self._record(request, 500, duration, request_id)
            raise

        duration = time.perf_counter() - started_at
        self._record(request, response.status_code, duration, request_id)
        response.headers["X-Request-ID"] = request_id
        return response

    @staticmethod
    def _record(request: Request, status_code: int, duration: float, request_id: str) -> None:
        path = request.url.path
        REQUEST_COUNT.labels(request.method, path, str(status_code)).inc()
        REQUEST_DURATION.labels(request.method, path).observe(duration)
        logger.info(json.dumps({
            "event": "http_request",
            "method": request.method,
            "path": path,
            "status_code": status_code,
            "duration_ms": round(duration * 1000, 2),
            "request_id": request_id,
        }))