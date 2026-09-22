import logging

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
from fastapi.security import OAuth2PasswordRequestForm
from prometheus_client import CONTENT_TYPE_LATEST

from app.core.auth import create_access_token
from app.core.config import settings
from app.core.errors import http_exception_handler, unhandled_exception_handler, validation_exception_handler
from app.middleware import RequestTelemetryMiddleware
from app.telemetry.metrics import render_metrics
from app.telemetry.otel import configure_telemetry
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

logging.basicConfig(level=logging.INFO, format="%(message)s")
configure_telemetry()

app = FastAPI(title=settings.app_name, version=settings.app_version, debug=settings.debug)
app.add_middleware(RequestTelemetryMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, unhandled_exception_handler)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "healthy"}


@app.get("/ready")
def ready() -> dict[str, str]:
    return {"status": "ready"}


@app.get("/version")
def version() -> dict[str, str]:
    return {"version": settings.app_version}


@app.get("/metrics", response_class=PlainTextResponse)
def metrics() -> PlainTextResponse:
    return PlainTextResponse(render_metrics(), media_type=CONTENT_TYPE_LATEST)


@app.post("/api/v1/auth/token")
def issue_token(form_data: OAuth2PasswordRequestForm = Depends()) -> dict[str, str]:
    return {"access_token": create_access_token(form_data.username), "token_type": "bearer"}
