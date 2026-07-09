"""Tests for telemetry schema constraints."""

from pydantic import ValidationError

from app.schemas.telemetry import TelemetryCreate


def test_telemetry_create_accepts_valid_payload() -> None:
    """Telemetry schema accepts valid operating values."""
    telemetry = TelemetryCreate(
        vehicle_id=1,
        vehicle_state="CRUISING",
        driving_mode="NORMAL",
        speed=80.0,
        rpm=2600,
        fuel_level=45.0,
        engine_temperature=95.0,
        battery_voltage=12.5,
        oil_life=70.0,
        coolant_level=65.0,
        tire_pressure_fl=33.0,
        tire_pressure_fr=33.0,
        tire_pressure_rl=33.0,
        tire_pressure_rr=33.0,
        brake_wear=20.0,
        engine_load=50.0,
        throttle_position=30.0,
        gear=4,
        trip_distance=12.4,
        odometer=5234.8,
        fuel_consumption=6.1,
    )
    assert telemetry.vehicle_id == 1
    assert telemetry.rpm == 2600


def test_telemetry_create_rejects_negative_speed() -> None:
    """Telemetry schema rejects invalid negative speed values."""
    try:
        TelemetryCreate(
            vehicle_id=1,
            vehicle_state="IDLE",
            driving_mode="ECO",
            speed=-1.0,
            rpm=1000,
            fuel_level=50.0,
            engine_temperature=90.0,
            battery_voltage=12.2,
            oil_life=75.0,
            coolant_level=70.0,
            tire_pressure_fl=33.0,
            tire_pressure_fr=33.0,
            tire_pressure_rl=33.0,
            tire_pressure_rr=33.0,
            brake_wear=10.0,
            engine_load=20.0,
            throttle_position=10.0,
            gear=1,
            trip_distance=1.0,
            odometer=100.0,
            fuel_consumption=4.5,
        )
    except ValidationError:
        assert True
    else:
        raise AssertionError("Expected ValidationError for negative speed")
