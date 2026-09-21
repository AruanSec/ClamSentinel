from __future__ import annotations

from pydantic import BaseModel, Field


class ScanCreate(BaseModel):
    filename: str = Field(..., min_length=1, max_length=255)
    sha256: str = Field(..., min_length=64, max_length=64)
    size_bytes: int = Field(..., ge=0)


class ScanRead(BaseModel):
    id: str
    filename: str
    sha256: str
    size_bytes: int
    status: str
    malware_name: str | None = None

    model_config = {"from_attributes": True}
