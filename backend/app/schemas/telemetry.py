"""Telemetry request and response schemas."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class TelemetryCreate(BaseModel):
    """Schema for creating telemetry records."""

    vehicle_id: int
    timestamp: datetime | None = None
    vehicle_state: str = Field(min_length=1, max_length=50)
    driving_mode: str = Field(min_length=1, max_length=50)
    speed: float = Field(ge=0, le=300)
    rpm: int = Field(ge=0, le=9000)
    fuel_level: float = Field(ge=0, le=100)
    engine_temperature: float = Field(ge=-20, le=180)
    battery_voltage: float = Field(ge=10.0, le=16.0)
    oil_life: float = Field(ge=0, le=100)
    coolant_level: float = Field(ge=0, le=100)
    tire_pressure_fl: float = Field(ge=0)
    tire_pressure_fr: float = Field(ge=0)
    tire_pressure_rl: float = Field(ge=0)
    tire_pressure_rr: float = Field(ge=0)
    brake_wear: float = Field(ge=0, le=100)
    engine_load: float = Field(ge=0, le=100)
    throttle_position: float = Field(ge=0, le=100)
    gear: int = Field(ge=0, le=8)
    trip_distance: float = Field(ge=0)
    odometer: float = Field(ge=0)
    fuel_consumption: float = Field(ge=0)

    model_config = ConfigDict(from_attributes=True)


class TelemetryResponse(BaseModel):
    """Schema returned for telemetry records."""

    id: int
    vehicle_id: int
    timestamp: datetime
    vehicle_state: str
    driving_mode: str
    speed: float
    rpm: int
    fuel_level: float
    engine_temperature: float
    battery_voltage: float
    oil_life: float
    coolant_level: float
    tire_pressure_fl: float
    tire_pressure_fr: float
    tire_pressure_rl: float
    tire_pressure_rr: float
    brake_wear: float
    engine_load: float
    throttle_position: float
    gear: int
    trip_distance: float
    odometer: float
    fuel_consumption: float
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TelemetryHistory(BaseModel):
    """Schema for telemetry history responses."""

    vehicle_id: int
    records: list[TelemetryResponse]

    model_config = ConfigDict(from_attributes=True)


class LatestTelemetry(BaseModel):
    """Schema for latest telemetry responses."""

    vehicle_id: int
    telemetry: TelemetryResponse | None

    model_config = ConfigDict(from_attributes=True)
