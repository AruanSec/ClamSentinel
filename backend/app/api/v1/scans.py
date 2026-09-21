from fastapi import APIRouter, HTTPException, status

from backend.app.schemas.scan import ScanCreate, ScanRead

router = APIRouter(prefix="/api/v1", tags=["scans"])


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "healthy"}


@router.get("/scans", response_model=list[ScanRead])
def list_scans() -> list[dict[str, str | int | None]]:
    return []


@router.post("/scans", response_model=ScanRead, status_code=status.HTTP_201_CREATED)
def create_scan(payload: ScanCreate) -> ScanRead:
    return ScanRead(
        id="placeholder-id",
        filename=payload.filename,
        sha256=payload.sha256,
        size_bytes=payload.size_bytes,
        status="queued",
        malware_name=None,
    )


@router.get("/scans/{scan_id}", response_model=ScanRead)
def get_scan(scan_id: str) -> ScanRead:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Scan not found")
