# API Examples

## Health

```bash
curl http://localhost:8000/api/v1/health
```

## Create Vehicle

```bash
curl -X POST http://localhost:8000/api/v1/vehicles \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Demo Car",
    "manufacturer": "Toyota",
    "model": "Corolla",
    "year": 2024,
    "fuel_type": "Petrol",
    "transmission": "Automatic",
    "odometer": 1200
  }'
```

## Create Telemetry

```bash
curl -X POST http://localhost:8000/api/v1/telemetry \
  -H "Content-Type: application/json" \
  -d '{
    "vehicle_id": 1,
    "vehicle_state": "CRUISING",
    "driving_mode": "NORMAL",
    "speed": 72.5,
    "rpm": 2300,
    "fuel_level": 58.2,
    "engine_temperature": 93.0,
    "battery_voltage": 12.6,
    "oil_life": 78.0,
    "coolant_level": 71.0,
    "tire_pressure_fl": 33.0,
    "tire_pressure_fr": 33.2,
    "tire_pressure_rl": 32.8,
    "tire_pressure_rr": 33.1,
    "brake_wear": 18.0,
    "engine_load": 45.0,
    "throttle_position": 28.0,
    "gear": 4,
    "trip_distance": 8.4,
    "odometer": 1208.4,
    "fuel_consumption": 6.3
  }'
```

## BON Chat

```bash
curl -X POST http://localhost:8000/api/v1/bon/chat \
  -H "Content-Type: application/json" \
  -d '{
    "vehicle_id": 1,
    "message": "Should I service my vehicle soon?",
    "session_id": "demo-session"
  }'
```

## WebSocket

Connect client to:

`ws://localhost:8000/api/v1/ws/telemetry/1`
