# Database Design

## Database Technology

Local development uses SQLite through SQLAlchemy 2.x. The session and model
configuration is portable to PostgreSQL by changing `DATABASE_URL`.

## Tables

### `vehicles`

Stores the registered vehicle identity and configuration: UUID, name,
manufacturer, model, year, fuel type, transmission, odometer, and timestamps.

### `telemetry`

Stores timestamped vehicle readings including vehicle state, driving mode,
speed, RPM, fuel, temperatures, battery, tires, braking, load, trip, and
odometer information. `vehicle_id` is a foreign key to `vehicles.id` and the
table has indexes for vehicle lookup and chronological history queries.

## Derived Data

Health, alert, maintenance, and prediction results are calculated at read time
from the latest telemetry. They are intentionally not database tables.
