from pydantic import BaseModel, Field, computed_field
from typing_extensions import Generic, TypeVar

T = TypeVar("T")


class PaginatedResponse(BaseModel, Generic[T]):
    """Generic paginated response model"""

    items: list[T]
    total: int = Field(0, ge=0, description="Total number of items")
    offset: int = Field(0, ge=0, description="Number of items to be skipped")
    limit: int = Field(100, ge=1, description="Maximum number of items to be returned")

    @computed_field
    @property
    def has_next(self) -> bool:
        return self.offset + self.limit < self.total

    @computed_field
    @property
    def has_previous(self) -> bool:
        return self.offset > 0

    @computed_field
    @property
    def total_pages(self) -> int:
        return (self.total + self.limit - 1) // self.limit

    @computed_field
    @property
    def current_page(self) -> int:
        return (self.offset // self.limit) + 1

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "items": [],
                    "total": 100,
                    "offset": 0,
                    "limit": 10,
                    "has_next": True,
                    "has_previous": False,
                    "total_pages": 1,
                    "current_page": 1,
                }
            ]
        }
    }


class PaginationParams(BaseModel):
    offset: int = Field(0, ge=0, description="Number of items to skip")
    limit: int = Field(10, ge=1, le=130, description="Max items to return")

    model_config = {"extra": "forbid"}
