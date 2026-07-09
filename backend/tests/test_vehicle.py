"""Tests for vehicle-related validation and service behavior."""

from app.schemas.vehicle import VehicleCreate, max_vehicle_year


def test_vehicle_create_accepts_valid_payload() -> None:
    """Vehicle schema accepts a realistic payload."""
    payload = VehicleCreate(
        name="Family Car",
        manufacturer="Toyota",
        model="Corolla",
        year=2024,
        fuel_type="Petrol",
        transmission="Automatic",
        odometer=12500.5,
    )
    assert payload.name == "Family Car"
    assert payload.odometer == 12500.5


def test_vehicle_create_rejects_out_of_range_year() -> None:
    """Vehicle schema rejects years outside allowed range."""
    invalid_year = max_vehicle_year() + 2
    try:
        VehicleCreate(
            name="Test",
            manufacturer="Brand",
            model="X",
            year=invalid_year,
            fuel_type="Petrol",
            transmission="Manual",
            odometer=0,
        )
    except ValueError as exc:
        assert "Year must be between" in str(exc)
    else:
        raise AssertionError("Expected ValueError for invalid vehicle year")
