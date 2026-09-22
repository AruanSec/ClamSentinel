from prometheus_client import Counter, Histogram, generate_latest

REQUEST_COUNT = Counter(
    "clamsentinel_http_requests_total",
    "Total HTTP requests",
    ("method", "path", "status"),
)
REQUEST_DURATION = Histogram(
    "clamsentinel_http_request_duration_seconds",
    "HTTP request duration in seconds",
    ("method", "path"),
)


def render_metrics() -> bytes:
    return generate_latest()