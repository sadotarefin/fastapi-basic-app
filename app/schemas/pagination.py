from typing_extensions import Generic, TypeVar
from pydantic import BaseModel, Field

T = TypeVar("T")

class PaginatedResponse(BaseModel, Generic[T]):
    """Generic paginated response model"""
    items: list[T]
    total: int = Field(0, ge=0, description="Total number of items")
    offset: int = Field(0, ge=0, description="Number of items to be skipped")
    limit: int = Field(100, ge=1, description="Maximum number of items to be returned")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "items": [],
                    "total": 100,
                    "offset": 0,
                    "limit": 10
                }
            ]
        }
    }

class PaginationParams(BaseModel):
    offset: int = Field(0, ge=0, description="Number of items to skip")
    limit: int = Field(10, ge=1, le=130, description="Max items to return")

    model_config = {"extra":"forbid"}
