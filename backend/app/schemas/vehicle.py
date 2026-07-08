"""Vehicle request and response schemas."""

from datetime import UTC, datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator


def max_vehicle_year() -> int:
    """Return the maximum accepted vehicle year."""
    return datetime.now(UTC).year + 1


class VehicleBase(BaseModel):
    """Shared vehicle fields."""

    name: str | None = Field(default=None, min_length=1, max_length=100)
    manufacturer: str | None = Field(default=None, min_length=1, max_length=100)
    model: str | None = Field(default=None, min_length=1, max_length=100)
    year: int | None = None
    fuel_type: str | None = Field(default=None, min_length=1, max_length=50)
    transmission: str | None = Field(default=None, min_length=1, max_length=50)
    odometer: float | None = Field(default=None, ge=0)

    @field_validator(
        "name",
        "manufacturer",
        "model",
        "fuel_type",
        "transmission",
    )
    @classmethod
    def validate_required_text(cls, value: str | None) -> str | None:
        """Reject blank strings when text fields are provided."""
        if value is not None and not value.strip():
            raise ValueError("Value cannot be blank")

        return value

    @field_validator("year")
    @classmethod
    def validate_year(cls, value: int | None) -> int | None:
        """Validate vehicle year bounds."""
        if value is not None and not 1900 <= value <= max_vehicle_year():
            raise ValueError(f"Year must be between 1900 and {max_vehicle_year()}")

        return value


class VehicleCreate(VehicleBase):
    """Schema for creating a vehicle."""

    name: str = Field(min_length=1, max_length=100)
    manufacturer: str = Field(min_length=1, max_length=100)
    model: str = Field(min_length=1, max_length=100)
    year: int
    fuel_type: str = Field(min_length=1, max_length=50)
    transmission: str = Field(min_length=1, max_length=50)
    odometer: float = Field(default=0, ge=0)


class VehicleUpdate(VehicleBase):
    """Schema for updating a vehicle."""


class VehicleResponse(BaseModel):
    """Schema returned for vehicle records."""

    id: int
    uuid: str
    name: str
    manufacturer: str
    model: str
    year: int
    fuel_type: str
    transmission: str
    odometer: float
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
