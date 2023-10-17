from typing import Optional
from pydantic import BaseModel


class StoreDTO(BaseModel):
    """
    DTO for store models.

    It returned when accessing store models from the API.
    """

    id: int
    name: str
    host: str
    phone: Optional[str]

    class Config:
        orm_mode = True


class StoreInputDTO(BaseModel):
    """DTO for creating new store model."""

    name: str
    phone: str