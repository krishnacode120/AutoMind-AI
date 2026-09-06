"""Integration coverage of browser-facing workflows using an isolated database."""

from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, select, func
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from app.core.app import create_app
from app.database.base import Base
from app.database.session import get_db
from app.events.event_bus import event_bus
from app.events.telemetry_events import TELEMETRY_CREATED
from app.models.telemetry import Telemetry
from app.models.vehicle import Vehicle


@pytest.fixture
def api_client(monkeypatch):
    """Never read or modify the developer's SQLite database."""
    from app.core import lifespan as lifecycle

    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    Base.metadata.create_all(engine)
    monkeypatch.setattr(lifecycle, "init_db", lambda: None)

    def session() -> Iterator[Session]:
        with Session(engine) as db:
            yield db

    application = create_app()
    application.dependency_overrides[get_db] = session
    with TestClient(application) as client:
        yield client, engine
    engine.dispose()


def create_vehicle(client, name="Integration car") -> int:
    """Create a valid vehicle through the API."""
    response = client.post(
        "/api/v1/vehicles",
        json={
            "name": name,
            "manufacturer": "Toyota",
            "model": "Corolla",
            "year": 2024,
            "fuel_type": "Petrol",
            "transmission": "Automatic",
            "odometer": 100,
        },
    )
    assert response.status_code == 201, response.text
    return response.json()["data"]["id"]


def test_complete_vehicle_drive_reports_chat_and_delete(api_client):
    """A newly created vehicle can complete the entire dashboard workflow."""
    client, engine = api_client
    vehicle_id = create_vehicle(client)
    base = f"/api/v1/vehicles/{vehicle_id}"
    assert client.get(base + "/health").status_code == 404
    response = client.post(base + "/simulation?samples=60")
    assert response.status_code == 201, response.text
    assert response.json()["data"]["samples"] == 60
    records = client.get(f"/api/v1/telemetry/history/{vehicle_id}").json()["data"][
        "records"
    ]
    assert len(records) == 60
    assert any(record["speed"] > 0 for record in records)
    assert records[0]["odometer"] > 100
    assert all(records[i]["odometer"] >= records[i + 1]["odometer"] for i in range(59))
    for endpoint in ("health", "alerts", "maintenance", "prediction"):
        response = client.get(base + "/" + endpoint)
        assert response.status_code == 200, response.text
        assert response.json()["data"]
    response = client.post(
        "/api/v1/bon/chat",
        json={
            "vehicle_id": vehicle_id,
            "message": "How is my car?",
            "session_id": "workflow",
        },
    )
    assert response.status_code == 200, response.text
    assert response.json()["context_used"]["vehicle"]["name"] == "Integration car"
    assert response.json()["context_used"]["telemetry"] is not None
    assert (
        len(client.get("/api/v1/bon/sessions/workflow").json()["data"]["history"]) == 2
    )
    assert client.delete("/api/v1/bon/sessions/workflow").status_code == 200
    assert client.get("/api/v1/bon/sessions/workflow").status_code == 404
    assert client.put(base, json={"name": "Renamed"}).status_code == 200
    assert client.put(base, json={"name": None}).status_code == 422
    assert client.get(base).json()["data"]["name"] == "Renamed"
    assert client.delete(base).status_code == 200
    with Session(engine) as db:
        assert db.scalar(select(func.count()).select_from(Telemetry)) == 0
        assert db.get(Vehicle, vehicle_id) is None


def test_rest_telemetry_publishes_serialized_event(api_client):
    """REST records must reach stream subscribers independently of ORM lifetime."""
    client, _ = api_client
    vehicle_id = create_vehicle(client)
    client.post(f"/api/v1/vehicles/{vehicle_id}/simulation?samples=1")
    record = client.get(f"/api/v1/telemetry/latest/{vehicle_id}").json()["data"][
        "telemetry"
    ]
    events = []
    event_bus.subscribe(TELEMETRY_CREATED, events.append)
    try:
        response = client.post("/api/v1/telemetry", json=record)
        assert response.status_code == 201, response.text
        assert events[0]["id"] == response.json()["data"]["id"]
        assert isinstance(events[0]["timestamp"], str)
    finally:
        event_bus.subscribers[TELEMETRY_CREATED].remove(events.append)


def test_missing_vehicle_invalid_inputs_and_docs(api_client):
    client, _ = api_client
    assert client.post("/api/v1/vehicles/999/simulation").status_code == 404
    vehicle_id = create_vehicle(client)
    for count in (0, 301):
        assert (
            client.post(
                f"/api/v1/vehicles/{vehicle_id}/simulation?samples={count}"
            ).status_code
            == 422
        )
    assert (
        client.post(
            "/api/v1/bon/chat",
            json={"vehicle_id": vehicle_id, "message": "  ", "session_id": "test"},
        ).status_code
        == 422
    )
    for path in ("/docs", "/redoc", "/api/v1/health"):
        assert client.get(path).status_code == 200


@pytest.mark.parametrize(
    "scenario,alert_type",
    [
        ("overheating", "HIGH_ENGINE_TEMP"),
        ("low_fuel", "LOW_FUEL"),
        ("worn_brakes", "HIGH_BRAKE_WEAR"),
    ],
)
def test_scenarios_feed_consistent_insights(api_client, scenario, alert_type):
    client, _ = api_client
    vehicle_id = create_vehicle(client)
    base = f"/api/v1/vehicles/{vehicle_id}"
    assert client.get(base + "/insights").status_code == 404
    response = client.post(base + f"/simulation?scenario={scenario}&samples=60")
    assert response.status_code == 201, response.text
    assert response.json()["data"]["scenario"] == scenario
    reports = client.get(base + "/insights").json()["data"]
    assert set(reports) == {"health", "alerts", "maintenance", "prediction"}
    assert alert_type in {alert["type"] for alert in reports["alerts"]["alerts"]}
    assert reports["health"]["health_score"] < 100
    assert reports["maintenance"]["task_count"] > 0
    assert (
        client.get(base + "/health").json()["data"]["health_score"]
        == reports["health"]["health_score"]
    )
    assert client.post(base + "/simulation?scenario=invalid").status_code == 422


def test_history_pagination_and_bounds(api_client):
    client, _ = api_client
    vehicle_id = create_vehicle(client, name="  Paged car  ")
    assert (
        client.get(f"/api/v1/vehicles/{vehicle_id}").json()["data"]["name"]
        == "Paged car"
    )
    client.post(f"/api/v1/vehicles/{vehicle_id}/simulation?samples=60")
    path = f"/api/v1/telemetry/history/{vehicle_id}"
    first = client.get(path + "?skip=0&limit=20").json()["data"]["records"]
    second = client.get(path + "?skip=20&limit=20").json()["data"]["records"]
    assert len(first) == len(second) == 20
    assert not {row["id"] for row in first} & {row["id"] for row in second}
    assert client.get(path + "?skip=60").json()["data"]["records"] == []
    for params in ("skip=-1", "limit=0", "limit=1001"):
        assert client.get(path + "?" + params).status_code == 422
        assert client.get("/api/v1/vehicles?" + params).status_code == 422


def test_timezone_normalization_keeps_latest_order_correct(api_client):
    client, _ = api_client
    vehicle_id = create_vehicle(client)
    client.post(f"/api/v1/vehicles/{vehicle_id}/simulation?samples=1")
    path = f"/api/v1/telemetry/latest/{vehicle_id}"
    record = client.get(path).json()["data"]["telemetry"]
    client.delete(f"/api/v1/telemetry/history/{vehicle_id}")
    record["timestamp"] = "2026-01-01T10:30:00+05:30"
    earlier = client.post("/api/v1/telemetry", json=record)
    assert earlier.status_code == 201
    record["timestamp"] = "2026-01-01T06:00:00Z"
    later = client.post("/api/v1/telemetry", json=record)
    assert later.status_code == 201
    latest = client.get(path).json()["data"]["telemetry"]
    assert latest["id"] == later.json()["data"]["id"]
    assert latest["timestamp"].endswith("+00:00")
