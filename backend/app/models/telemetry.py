"""Telemetry database model."""

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Float, ForeignKey, Index, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.utils.time_utils import utc_now

if TYPE_CHECKING:
    from app.models.vehicle import Vehicle


class Telemetry(Base):
    """Vehicle telemetry snapshot stored in the database."""

    __tablename__ = "telemetry"
    __table_args__ = (
        Index("ix_telemetry_vehicle_timestamp", "vehicle_id", "timestamp"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    vehicle_id: Mapped[int] = mapped_column(
        ForeignKey("vehicles.id"),
        nullable=False,
        index=True,
    )
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
        index=True,
    )
    vehicle_state: Mapped[str] = mapped_column(String(50), nullable=False)
    driving_mode: Mapped[str] = mapped_column(String(50), nullable=False)
    speed: Mapped[float] = mapped_column(Float, nullable=False)
    rpm: Mapped[int] = mapped_column(Integer, nullable=False)
    fuel_level: Mapped[float] = mapped_column(Float, nullable=False)
    engine_temperature: Mapped[float] = mapped_column(Float, nullable=False)
    battery_voltage: Mapped[float] = mapped_column(Float, nullable=False)
    oil_life: Mapped[float] = mapped_column(Float, nullable=False)
    coolant_level: Mapped[float] = mapped_column(Float, nullable=False)
    tire_pressure_fl: Mapped[float] = mapped_column(Float, nullable=False)
    tire_pressure_fr: Mapped[float] = mapped_column(Float, nullable=False)
    tire_pressure_rl: Mapped[float] = mapped_column(Float, nullable=False)
    tire_pressure_rr: Mapped[float] = mapped_column(Float, nullable=False)
    brake_wear: Mapped[float] = mapped_column(Float, nullable=False)
    engine_load: Mapped[float] = mapped_column(Float, nullable=False)
    throttle_position: Mapped[float] = mapped_column(Float, nullable=False)
    gear: Mapped[int] = mapped_column(Integer, nullable=False)
    trip_distance: Mapped[float] = mapped_column(Float, nullable=False)
    odometer: Mapped[float] = mapped_column(Float, nullable=False)
    fuel_consumption: Mapped[float] = mapped_column(Float, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
    )

    vehicle: Mapped["Vehicle"] = relationship("Vehicle")
