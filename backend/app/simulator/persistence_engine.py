"""Persistence engine for simulation snapshots."""

from sqlalchemy.orm import Session

from app.models.telemetry import Telemetry
from app.models.vehicle import Vehicle
from app.simulator.simulation_controller import SimulationController
from app.simulator.simulation_models import SimulationSnapshot


DEFAULT_FUEL_CONSUMPTION = 0.0


class PersistenceEngine:
    """Persist simulation snapshots as telemetry records."""

    def __init__(self, db: Session) -> None:
        """Initialize the persistence engine."""
        self._db = db

    def save_snapshot(
        self,
        vehicle_id: int,
        snapshot: SimulationSnapshot,
    ) -> Telemetry:
        """Save one simulation snapshot as a telemetry record."""
        vehicle = self._get_vehicle_or_raise(vehicle_id)
        telemetry = self._build_telemetry(vehicle, snapshot)

        self._db.add(telemetry)
        self._db.commit()
        self._db.refresh(telemetry)
        return telemetry

    def save_many(
        self,
        vehicle_id: int,
        snapshots: list[SimulationSnapshot],
    ) -> list[Telemetry]:
        """Save multiple simulation snapshots and commit once."""
        vehicle = self._get_vehicle_or_raise(vehicle_id)
        telemetry_records = [
            self._build_telemetry(vehicle, snapshot)
            for snapshot in snapshots
        ]

        self._db.add_all(telemetry_records)
        self._db.commit()

        for telemetry in telemetry_records:
            self._db.refresh(telemetry)

        return telemetry_records

    def _get_vehicle_or_raise(self, vehicle_id: int) -> Vehicle:
        """Return a vehicle or raise ValueError when missing."""
        vehicle = self._db.get(Vehicle, vehicle_id)
        if vehicle is None:
            raise ValueError(f"Vehicle with id {vehicle_id} does not exist")

        return vehicle

    def _build_telemetry(
        self,
        vehicle: Vehicle,
        snapshot: SimulationSnapshot,
    ) -> Telemetry:
        """Convert a simulation snapshot into a Telemetry ORM object."""
        return Telemetry(
            vehicle_id=vehicle.id,
            timestamp=snapshot.timestamp,
            vehicle_state=snapshot.vehicle_state,
            driving_mode=snapshot.driving_mode,
            speed=snapshot.speed,
            rpm=snapshot.rpm,
            fuel_level=snapshot.fuel_level,
            engine_temperature=snapshot.engine_temperature,
            battery_voltage=snapshot.battery_voltage,
            oil_life=snapshot.oil_life,
            coolant_level=snapshot.coolant_level,
            tire_pressure_fl=snapshot.tire_pressure_fl,
            tire_pressure_fr=snapshot.tire_pressure_fr,
            tire_pressure_rl=snapshot.tire_pressure_rl,
            tire_pressure_rr=snapshot.tire_pressure_rr,
            brake_wear=snapshot.brake_wear,
            engine_load=snapshot.engine_load,
            throttle_position=snapshot.throttle_position,
            gear=snapshot.gear,
            trip_distance=snapshot.distance_delta,
            odometer=vehicle.odometer + snapshot.distance_delta,
            fuel_consumption=DEFAULT_FUEL_CONSUMPTION,
        )


def simulate_once(
    vehicle_id: int,
    controller: SimulationController,
    persistence: PersistenceEngine,
) -> Telemetry:
    """Run one simulation step and persist the resulting snapshot."""
    snapshot = controller.step()
    return persistence.save_snapshot(vehicle_id, snapshot)
