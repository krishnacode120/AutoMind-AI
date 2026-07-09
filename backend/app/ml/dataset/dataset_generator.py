"""Machine learning dataset generation from the existing simulator."""

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from app.ml.dataset.csv_exporter import CSVExporter
from app.ml.dataset.dataset_statistics import DatasetStatistics
from app.ml.dataset.feature_engineering import FeatureEngineer
from app.ml.dataset.label_generator import FailureLabelGenerator
from app.ml.scenarios.driving_profiles import DrivingProfile
from app.ml.scenarios.fault_injector import FaultInjector
from app.ml.scenarios.scenario import FaultType, Scenario
from app.ml.scenarios.scenario_generator import ScenarioGenerator
from app.models.telemetry import Telemetry
from app.prediction.rule_predictor import RuleBasedPredictor
from app.services.alert_service import VehicleAlertService
from app.services.health_service import VehicleHealthService
from app.services.maintenance_service import VehicleMaintenanceService
from app.simulator.enums import VehicleState
from app.simulator.physics_engine import PhysicsEngine
from app.simulator.runner import SimulationRunner
from app.simulator.sensor_engine import SensorEngine
from app.simulator.simulation_controller import SimulationController
from app.simulator.simulation_models import SimulationSnapshot
from app.simulator.state_machine import VehicleStateMachine
from app.utils.time_utils import utc_now


DEFAULT_DATASET_SIZE = 10_000
DEFAULT_VEHICLE_ID = 1
DEFAULT_INTERVAL_SECONDS = 0.0
DEFAULT_FUEL_CONSUMPTION = 0.0


@dataclass(frozen=True)
class DatasetGenerationResult:
    """Generated dataset rows with summary metadata."""

    rows: list[dict[str, Any]]
    statistics: dict[str, Any]
    csv_path: Path | None = None


class DatasetGenerator:
    """Generate deterministic ML datasets from simulator output."""

    def __init__(
        self,
        vehicle_id: int = DEFAULT_VEHICLE_ID,
        random_seed: int | None = 0,
        profile_weights: dict[str, float] | None = None,
        fault_probabilities: dict[FaultType | str, float] | None = None,
    ) -> None:
        """Initialize generator services and simulator components."""
        self.vehicle_id = vehicle_id
        self._state_machine = VehicleStateMachine()
        self._physics_engine = PhysicsEngine(self._state_machine)
        self._sensor_engine = SensorEngine(
            self._physics_engine,
            random_seed=random_seed,
        )
        self._controller = SimulationController(
            state_machine=self._state_machine,
            physics_engine=self._physics_engine,
            sensor_engine=self._sensor_engine,
        )
        self._persistence = _DatasetPersistenceEngine(vehicle_id)
        self._runner = SimulationRunner(
            vehicle_id=vehicle_id,
            controller=self._controller,
            persistence=self._persistence,
            interval_seconds=DEFAULT_INTERVAL_SECONDS,
        )
        self._feature_engineer = FeatureEngineer()
        self._label_generator = FailureLabelGenerator()
        self._health_service = VehicleHealthService()
        self._alert_service = VehicleAlertService()
        self._maintenance_service = VehicleMaintenanceService()
        self._predictor = RuleBasedPredictor()
        self._statistics = DatasetStatistics()
        self._csv_exporter = CSVExporter()
        self._scenario_generator = ScenarioGenerator(
            profile_weights=profile_weights,
            fault_probabilities=fault_probabilities,
            random_seed=random_seed,
        )
        self._fault_injector = FaultInjector(random_seed=random_seed)

    def generate(
        self,
        size: int = DEFAULT_DATASET_SIZE,
        output_path: str | Path | None = None,
    ) -> DatasetGenerationResult:
        """Generate dataset rows and optionally export them to CSV."""
        if size < 0:
            raise ValueError("Dataset size must be greater than or equal to 0")

        self._prepare_vehicle_state()
        rows = [self._generate_row(index) for index in range(size)]
        statistics = self._statistics.summarize(rows)
        csv_path = (
            self._csv_exporter.export(rows, output_path)
            if output_path is not None
            else None
        )

        return DatasetGenerationResult(
            rows=rows,
            statistics=statistics,
            csv_path=csv_path,
        )

    def export_csv(
        self,
        rows: list[dict[str, Any]],
        output_path: str | Path,
    ) -> Path:
        """Export existing dataset rows to CSV."""
        return self._csv_exporter.export(rows, output_path)

    def summarize(self, rows: list[dict[str, Any]]) -> dict[str, Any]:
        """Return dataset statistics for existing rows."""
        return self._statistics.summarize(rows)

    def _generate_row(self, index: int) -> dict[str, Any]:
        """Generate one dataset row from a simulator step."""
        scenario = self._scenario_generator.generate()
        self._state_machine.set_mode(scenario.profile.driving_mode)
        self._advance_state(index, scenario.profile)
        self._runner.step_once()
        telemetry = self._fault_injector.inject(
            self._persistence.latest(),
            scenario,
        )
        health_report = self._health_service.calculate_health(telemetry)
        alert_report = self._alert_service.generate_alerts(
            telemetry,
            health_report,
        )
        maintenance_report = self._maintenance_service.generate_maintenance_plan(
            telemetry,
            health_report,
            alert_report,
        )
        prediction = self._predictor.predict(
            health_report,
            alert_report,
            maintenance_report,
        )

        row = self._feature_engineer.build_features(
            telemetry=telemetry,
            health_report=health_report,
            alert_report=alert_report,
            maintenance_report=maintenance_report,
            prediction=prediction,
            scenario_profile=scenario.profile.name,
            injected_faults=self._fault_names(scenario),
        )
        row["failure"] = self._label_generator.generate(
            health_report=health_report,
            alert_report=alert_report,
            maintenance_report=maintenance_report,
            prediction=prediction,
        )
        return row

    def _prepare_vehicle_state(self) -> None:
        """Move the state machine from OFF to IDLE before sampling."""
        if self._state_machine.current_state() == VehicleState.OFF:
            self._controller.start()

        if self._state_machine.current_state() == VehicleState.STARTING:
            self._controller.start()

    def _advance_state(self, index: int, profile: DrivingProfile) -> None:
        """Apply valid state transitions for repeatable driving cycles."""
        cycle_position = index % profile.cycle_length
        current_state = self._state_machine.current_state()

        if current_state == VehicleState.IDLE:
            self._controller.accelerate()
            return

        if (
            current_state == VehicleState.ACCELERATING
            and cycle_position >= profile.acceleration_steps
        ):
            self._controller.cruise()
            return

        if (
            current_state == VehicleState.CRUISING
            and cycle_position
            >= profile.acceleration_steps + profile.cruising_steps
        ):
            self._controller.brake()
            return

        if (
            current_state == VehicleState.BRAKING
            and cycle_position
            >= (
                profile.acceleration_steps
                + profile.cruising_steps
                + profile.braking_steps
            )
        ):
            self._controller.stop()
            return

        if current_state == VehicleState.STOPPED:
            self._controller.stop()

    def _fault_names(self, scenario: Scenario) -> tuple[str, ...]:
        """Return fault names for dataset metadata."""
        return tuple(fault.value for fault in scenario.faults)


class _DatasetPersistenceEngine:
    """In-memory persistence adapter for SimulationRunner dataset steps."""

    def __init__(self, vehicle_id: int) -> None:
        """Initialize in-memory telemetry storage."""
        self.vehicle_id = vehicle_id
        self._next_id = 1
        self._odometer = 0.0
        self.records: list[Telemetry] = []

    def save_snapshot(
        self,
        vehicle_id: int,
        snapshot: SimulationSnapshot,
    ) -> Telemetry:
        """Convert a simulation snapshot to an unsaved Telemetry object."""
        if vehicle_id != self.vehicle_id:
            raise ValueError(f"Unknown dataset vehicle id: {vehicle_id}")

        self._odometer += snapshot.distance_delta
        telemetry = self._build_telemetry(vehicle_id, snapshot)
        self.records.append(telemetry)
        return telemetry

    def save_many(
        self,
        vehicle_id: int,
        snapshots: list[SimulationSnapshot],
    ) -> list[Telemetry]:
        """Convert many snapshots to unsaved Telemetry objects."""
        return [
            self.save_snapshot(vehicle_id, snapshot)
            for snapshot in snapshots
        ]

    def latest(self) -> Telemetry:
        """Return the most recently captured telemetry record."""
        if not self.records:
            raise RuntimeError("No telemetry records have been generated")

        return self.records[-1]

    def _build_telemetry(
        self,
        vehicle_id: int,
        snapshot: SimulationSnapshot,
    ) -> Telemetry:
        """Build a telemetry model instance from a simulation snapshot."""
        telemetry = Telemetry(
            id=self._next_id,
            vehicle_id=vehicle_id,
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
            odometer=round(self._odometer, 6),
            fuel_consumption=DEFAULT_FUEL_CONSUMPTION,
            created_at=utc_now(),
        )
        self._next_id += 1
        return telemetry
