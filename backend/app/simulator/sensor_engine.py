"""Vehicle sensor engine."""

from random import Random

from app.simulator.physics_engine import (
    ENGINE_OFF_RPM,
    IDLE_RPM,
    MAX_ACCELERATION_DELTA,
    MAX_BRAKING_DELTA,
    MAX_SPEED,
    PhysicsEngine,
    STARTING_RPM,
)
from app.simulator.physics_models import PhysicsSnapshot
from app.simulator.sensor_models import SensorSnapshot


AMBIENT_TEMPERATURE = 25.0
IDLE_TEMPERATURE_TARGET = 80.0
STARTING_TEMPERATURE_TARGET = 65.0
ACCELERATION_TEMPERATURE_BASE = 92.0
ACCELERATION_TEMPERATURE_LOAD_FACTOR = 0.14
CRUISING_TEMPERATURE_MIN = 88.0
CRUISING_TEMPERATURE_RANGE = 7.0
BRAKING_TEMPERATURE_TARGET = 86.0
MAX_TEMPERATURE_CHANGE = 2.0

BATTERY_OFF_VOLTAGE = 12.3
BATTERY_STARTING_VOLTAGE = 12.0
BATTERY_RUNNING_BASE = 14.1
BATTERY_RUNNING_VARIATION = 0.3
MAX_BATTERY_CHANGE = 0.12

MAX_PERCENT = 100.0
MIN_PERCENT = 0.0
INITIAL_FUEL_LEVEL = 100.0
INITIAL_OIL_LIFE = 100.0
INITIAL_COOLANT_LEVEL = 100.0
INITIAL_BRAKE_WEAR = 0.0

BASE_FUEL_USAGE = 0.0003
RPM_FUEL_USAGE_FACTOR = 0.002
THROTTLE_FUEL_USAGE_FACTOR = 0.001
MAX_RPM = 9000.0

OIL_DISTANCE_INTERVAL = 10.0
OIL_DISTANCE_DECREASE = 0.01
COOLANT_DISTANCE_INTERVAL = 100.0
COOLANT_DISTANCE_DECREASE = 0.01

TIRE_PRESSURE_MIN = 32.0
TIRE_PRESSURE_MAX = 35.0
TIRE_PRESSURE_DRIFT = 0.02
INITIAL_TIRE_PRESSURES = {
    "fl": 33.4,
    "fr": 33.5,
    "rl": 33.1,
    "rr": 33.2,
}

IDLE_THROTTLE = 3.0
ACCELERATION_THROTTLE_MIN = 30.0
ACCELERATION_THROTTLE_RANGE = 60.0
CRUISING_THROTTLE_MIN = 15.0
CRUISING_THROTTLE_RANGE = 20.0
ZERO_THROTTLE = 0.0

IDLE_ENGINE_LOAD = 8.0
RPM_LOAD_FACTOR = 50.0
THROTTLE_LOAD_FACTOR = 0.45
ACCELERATION_LOAD_BONUS = 20.0
CRUISING_LOAD_BONUS = 5.0

DEFAULT_RANDOM_SEED = 0


class SensorEngine:
    """Calculate realistic sensor readings from physics snapshots."""

    def __init__(
        self,
        physics_engine: PhysicsEngine,
        random_seed: int | None = DEFAULT_RANDOM_SEED,
    ) -> None:
        """Initialize the sensor engine."""
        self._physics_engine = physics_engine
        self._random = Random(random_seed)
        self.temperature = AMBIENT_TEMPERATURE
        self.battery = BATTERY_OFF_VOLTAGE
        self.fuel = INITIAL_FUEL_LEVEL
        self.oil = INITIAL_OIL_LIFE
        self.coolant = INITIAL_COOLANT_LEVEL
        self.tire_pressure_fl = INITIAL_TIRE_PRESSURES["fl"]
        self.tire_pressure_fr = INITIAL_TIRE_PRESSURES["fr"]
        self.tire_pressure_rl = INITIAL_TIRE_PRESSURES["rl"]
        self.tire_pressure_rr = INITIAL_TIRE_PRESSURES["rr"]
        self.brake_wear = INITIAL_BRAKE_WEAR
        self._oil_distance = 0.0
        self._coolant_distance = 0.0
        self._update_count = 0

    def update(
        self,
        physics_snapshot: PhysicsSnapshot | None = None,
    ) -> SensorSnapshot:
        """Update sensor readings from a physics snapshot."""
        self._update_count += 1
        snapshot = physics_snapshot or self._physics_engine.update()
        throttle = self._calculate_throttle(snapshot)

        self._update_temperature(snapshot)
        self._update_battery(snapshot)
        self._update_fuel(snapshot, throttle)
        self._update_oil(snapshot.distance_delta)
        self._update_coolant(snapshot.distance_delta)
        self._update_tire_pressures()
        self._update_brake_wear(snapshot)
        engine_load = self._calculate_engine_load(snapshot, throttle)

        return SensorSnapshot(
            engine_temperature=round(self.temperature, 2),
            battery_voltage=round(self.battery, 2),
            fuel_level=round(self.fuel, 4),
            oil_life=round(self.oil, 4),
            coolant_level=round(self.coolant, 4),
            tire_pressure_fl=round(self.tire_pressure_fl, 2),
            tire_pressure_fr=round(self.tire_pressure_fr, 2),
            tire_pressure_rl=round(self.tire_pressure_rl, 2),
            tire_pressure_rr=round(self.tire_pressure_rr, 2),
            brake_wear=round(self.brake_wear, 4),
            engine_load=round(engine_load, 2),
            throttle_position=round(throttle, 2),
        )

    def _update_temperature(self, snapshot: PhysicsSnapshot) -> None:
        """Move engine temperature smoothly toward the target."""
        target = self._temperature_target(snapshot)
        self.temperature = self._approach(
            current=self.temperature,
            target=target,
            max_delta=MAX_TEMPERATURE_CHANGE,
        )

    def _temperature_target(self, snapshot: PhysicsSnapshot) -> float:
        """Return target engine temperature for current movement."""
        if not snapshot.engine_running:
            return AMBIENT_TEMPERATURE

        if snapshot.rpm == STARTING_RPM and snapshot.speed == 0:
            return STARTING_TEMPERATURE_TARGET

        if snapshot.speed == 0:
            return IDLE_TEMPERATURE_TARGET

        if snapshot.acceleration > 0:
            return ACCELERATION_TEMPERATURE_BASE + (
                self._calculate_throttle(snapshot)
                * ACCELERATION_TEMPERATURE_LOAD_FACTOR
            )

        if snapshot.acceleration < 0:
            return BRAKING_TEMPERATURE_TARGET

        speed_ratio = min(snapshot.speed / MAX_SPEED, 1.0)
        return CRUISING_TEMPERATURE_MIN + (
            CRUISING_TEMPERATURE_RANGE * speed_ratio
        )

    def _update_battery(self, snapshot: PhysicsSnapshot) -> None:
        """Move battery voltage smoothly toward the target."""
        target = self._battery_target(snapshot)
        self.battery = self._approach(
            current=self.battery,
            target=target,
            max_delta=MAX_BATTERY_CHANGE,
        )

    def _battery_target(self, snapshot: PhysicsSnapshot) -> float:
        """Return target battery voltage for current engine state."""
        if not snapshot.engine_running:
            return BATTERY_OFF_VOLTAGE

        if snapshot.rpm == STARTING_RPM:
            return BATTERY_STARTING_VOLTAGE

        return BATTERY_RUNNING_BASE + self._smooth_variation(
            BATTERY_RUNNING_VARIATION,
        )

    def _update_fuel(
        self,
        snapshot: PhysicsSnapshot,
        throttle: float,
    ) -> None:
        """Decrease fuel slowly based on RPM and throttle."""
        if not snapshot.engine_running:
            return

        rpm_factor = snapshot.rpm / MAX_RPM
        throttle_factor = throttle / MAX_PERCENT
        fuel_used = (
            BASE_FUEL_USAGE
            + (rpm_factor * RPM_FUEL_USAGE_FACTOR)
            + (throttle_factor * THROTTLE_FUEL_USAGE_FACTOR)
        )
        self.fuel = self._clamp(self.fuel - fuel_used, MIN_PERCENT, MAX_PERCENT)

    def _update_oil(self, distance_delta: float) -> None:
        """Decrease oil life over accumulated distance."""
        self._oil_distance += distance_delta
        if self._oil_distance < OIL_DISTANCE_INTERVAL:
            return

        intervals = int(self._oil_distance // OIL_DISTANCE_INTERVAL)
        self._oil_distance -= intervals * OIL_DISTANCE_INTERVAL
        self.oil = self._clamp(
            self.oil - (intervals * OIL_DISTANCE_DECREASE),
            MIN_PERCENT,
            MAX_PERCENT,
        )

    def _update_coolant(self, distance_delta: float) -> None:
        """Decrease coolant level very slowly over long distance."""
        self._coolant_distance += distance_delta
        if self._coolant_distance < COOLANT_DISTANCE_INTERVAL:
            return

        intervals = int(self._coolant_distance // COOLANT_DISTANCE_INTERVAL)
        self._coolant_distance -= intervals * COOLANT_DISTANCE_INTERVAL
        self.coolant = self._clamp(
            self.coolant - (intervals * COOLANT_DISTANCE_DECREASE),
            MIN_PERCENT,
            MAX_PERCENT,
        )

    def _update_tire_pressures(self) -> None:
        """Apply tiny deterministic random drift to tire pressure."""
        self.tire_pressure_fl = self._drift_tire_pressure(self.tire_pressure_fl)
        self.tire_pressure_fr = self._drift_tire_pressure(self.tire_pressure_fr)
        self.tire_pressure_rl = self._drift_tire_pressure(self.tire_pressure_rl)
        self.tire_pressure_rr = self._drift_tire_pressure(self.tire_pressure_rr)

    def _drift_tire_pressure(self, pressure: float) -> float:
        """Return tire pressure after a tiny bounded drift."""
        drift = self._random.uniform(-TIRE_PRESSURE_DRIFT, TIRE_PRESSURE_DRIFT)
        return self._clamp(
            pressure + drift,
            TIRE_PRESSURE_MIN,
            TIRE_PRESSURE_MAX,
        )

    def _update_brake_wear(self, snapshot: PhysicsSnapshot) -> None:
        """Increase brake wear only while braking."""
        if snapshot.acceleration >= 0:
            return

        braking_intensity = abs(snapshot.acceleration / MAX_BRAKING_DELTA)
        self.brake_wear = self._clamp(
            self.brake_wear + (braking_intensity * 0.01),
            MIN_PERCENT,
            MAX_PERCENT,
        )

    def _calculate_throttle(self, snapshot: PhysicsSnapshot) -> float:
        """Calculate throttle position from movement state."""
        if not snapshot.engine_running:
            return ZERO_THROTTLE

        if snapshot.rpm == STARTING_RPM and snapshot.speed == 0:
            return ZERO_THROTTLE

        if snapshot.acceleration < 0:
            return ZERO_THROTTLE

        if snapshot.speed == 0 and snapshot.rpm >= IDLE_RPM:
            return IDLE_THROTTLE

        if snapshot.acceleration > 0:
            acceleration_ratio = min(
                snapshot.acceleration / MAX_ACCELERATION_DELTA,
                1.0,
            )
            return ACCELERATION_THROTTLE_MIN + (
                ACCELERATION_THROTTLE_RANGE * acceleration_ratio
            )

        speed_ratio = min(snapshot.speed / MAX_SPEED, 1.0)
        return CRUISING_THROTTLE_MIN + (CRUISING_THROTTLE_RANGE * speed_ratio)

    def _calculate_engine_load(
        self,
        snapshot: PhysicsSnapshot,
        throttle: float,
    ) -> float:
        """Calculate engine load from RPM, throttle, and movement."""
        if not snapshot.engine_running or snapshot.rpm == ENGINE_OFF_RPM:
            return MIN_PERCENT

        if snapshot.speed == 0 and snapshot.rpm >= IDLE_RPM:
            return IDLE_ENGINE_LOAD

        rpm_load = (snapshot.rpm / MAX_RPM) * RPM_LOAD_FACTOR
        throttle_load = throttle * THROTTLE_LOAD_FACTOR
        movement_bonus = self._movement_load_bonus(snapshot)
        return self._clamp(
            rpm_load + throttle_load + movement_bonus,
            MIN_PERCENT,
            MAX_PERCENT,
        )

    def _movement_load_bonus(self, snapshot: PhysicsSnapshot) -> float:
        """Return engine load bonus from movement state."""
        if snapshot.acceleration > 0:
            return ACCELERATION_LOAD_BONUS

        if snapshot.acceleration == 0 and snapshot.speed > 0:
            return CRUISING_LOAD_BONUS

        return MIN_PERCENT

    def _smooth_variation(self, magnitude: float) -> float:
        """Return a small deterministic oscillating variation."""
        return magnitude if self._update_count % 2 == 0 else -magnitude

    def _approach(
        self,
        current: float,
        target: float,
        max_delta: float,
    ) -> float:
        """Move a value toward a target by at most max_delta."""
        delta = target - current
        bounded_delta = self._clamp(delta, -max_delta, max_delta)
        return current + bounded_delta

    def _clamp(self, value: float, minimum: float, maximum: float) -> float:
        """Clamp a value to an inclusive range."""
        return max(minimum, min(value, maximum))
