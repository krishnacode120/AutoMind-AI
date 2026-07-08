"""Simulation runner lifecycle management."""

from threading import Event, Lock, Thread, current_thread
from time import sleep

from app.simulator.persistence_engine import PersistenceEngine
from app.simulator.simulation_controller import SimulationController
from app.simulator.simulation_models import SimulationSnapshot


PAUSED_SLEEP_SECONDS = 0.1
DEFAULT_INTERVAL_SECONDS = 1.0


class SimulationRunner:
    """Run simulation steps on a managed background thread."""

    def __init__(
        self,
        vehicle_id: int,
        controller: SimulationController,
        persistence: PersistenceEngine,
        interval_seconds: float = DEFAULT_INTERVAL_SECONDS,
    ) -> None:
        """Initialize the simulation runner."""
        self.vehicle_id = vehicle_id
        self.controller = controller
        self.persistence = persistence
        self.interval_seconds = interval_seconds
        self.running = False
        self.paused = False
        self.step_count = 0
        self.last_error: Exception | None = None
        self._thread: Thread | None = None
        self._lock = Lock()
        self._stop_event = Event()

    def start(self) -> None:
        """Start the simulation loop on a background thread."""
        with self._lock:
            if self.running or self._thread_is_alive():
                raise RuntimeError("Simulation runner is already running")

            self.running = True
            self.paused = False
            self.last_error = None
            self._stop_event.clear()
            self._thread = Thread(target=self.run, daemon=True)
            self._thread.start()

    def stop(self) -> None:
        """Stop the simulation loop and wait for the thread to finish."""
        thread = self._thread
        self._stop_event.set()

        with self._lock:
            self.running = False
            self.paused = False

        if (
            thread is not None
            and thread.is_alive()
            and thread is not current_thread()
        ):
            thread.join()

        with self._lock:
            self._thread = None

    def pause(self) -> None:
        """Pause simulation stepping without terminating the thread."""
        with self._lock:
            if self.running:
                self.paused = True

    def resume(self) -> None:
        """Resume simulation stepping after a pause."""
        with self._lock:
            if self.running:
                self.paused = False

    def step_once(self) -> SimulationSnapshot:
        """Run and persist a single simulation step."""
        snapshot = self.controller.step()
        self.persistence.save_snapshot(self.vehicle_id, snapshot)
        self.step_count += 1
        return snapshot

    def run(self) -> None:
        """Run simulation steps until stopped."""
        try:
            while self.running and not self._stop_event.is_set():
                if self.paused:
                    sleep(PAUSED_SLEEP_SECONDS)
                    continue

                self.step_once()
                self._stop_event.wait(self.interval_seconds)
        except Exception as exc:
            self.last_error = exc
            self._stop_cleanly()
        finally:
            self._stop_cleanly()

    def _stop_cleanly(self) -> None:
        """Mark the runner as stopped without joining the current thread."""
        with self._lock:
            self.running = False
            self.paused = False
            self._stop_event.set()

    def _thread_is_alive(self) -> bool:
        """Return whether this runner already has a live thread."""
        return self._thread is not None and self._thread.is_alive()
