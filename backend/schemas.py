from datetime import datetime
from pydantic import BaseModel, ConfigDict


class PipeBase(BaseModel):
    pipe_code: str
    material: str
    installation_year: int | None = None
    diameter_mm: float | None = None
    length_m: float | None = None
    location: str | None = None
    corrosion_level: float | None = None
    previous_failures: int = 0
    status: str = "active"
    latitude: float | None = None
    longitude: float | None = None


class PipeCreate(PipeBase):
    pass


class PipeResponse(PipeBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)