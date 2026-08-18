import PageHeader from "../components/common/PageHeader";
import Card from "../components/common/Card";
import Loading from "../components/common/Loading";
import TelemetryCharts from "../components/charts/TelemetryCharts";
import { usePrimaryVehicle } from "../hooks/usePrimaryVehicle";
import { useLatestTelemetry } from "../hooks/useTelemetry";

function Telemetry() {
  const { vehicle, vehicleId, isLoading: vehiclesLoading } = usePrimaryVehicle();
  const { data, isLoading, isError } = useLatestTelemetry(vehicleId ?? 0);
  const telemetry = data?.telemetry;

  return (
    <div className="resource-page">
      <PageHeader
        title="Telemetry"
        subtitle={vehicle ? `Live reading for ${vehicle.name}` : "Vehicle sensor readings"}
      />
      {(vehiclesLoading || isLoading) && <Loading />}
      {!vehiclesLoading && !vehicle && <Card className="resource-card"><p className="resource-empty">Add a vehicle to view telemetry.</p></Card>}
      {isError && <Card className="resource-card"><p className="resource-empty">Telemetry is unavailable.</p></Card>}
      {telemetry && (
        <>
          <Card className="resource-card">
            <div className="detail-grid">
              <Metric label="Speed" value={`${telemetry.speed.toFixed(1)} km/h`} />
              <Metric label="Engine speed" value={`${telemetry.rpm} RPM`} />
              <Metric label="Gear" value={String(telemetry.gear)} />
              <Metric label="Fuel" value={`${telemetry.fuel_level.toFixed(1)}%`} />
              <Metric label="Temperature" value={`${telemetry.engine_temperature.toFixed(1)} C`} />
              <Metric label="Odometer" value={`${telemetry.odometer.toLocaleString()} km`} />
            </div>
          </Card>
          {vehicleId && <TelemetryCharts vehicleId={vehicleId} />}
        </>
      )}
    </div>
  );
}

function Metric({ label, value }: { label: string; value: string }) {
  return <div className="metric"><span>{label}</span><strong>{value}</strong></div>;
}

export default Telemetry;
