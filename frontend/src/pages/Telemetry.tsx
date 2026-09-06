import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { ChevronLeft, ChevronRight, Download } from "lucide-react";
import PageHeader from "../components/common/PageHeader";
import EmptyState from "../components/common/EmptyState";
import Loading from "../components/common/Loading";
import TelemetryCharts from "../components/charts/TelemetryCharts";
import SimulateDrive from "../components/common/SimulateDrive";
import { usePrimaryVehicle } from "../hooks/usePrimaryVehicle";
import { useLatestTelemetry } from "../hooks/useTelemetry";
import { getTelemetryHistory } from "../services/telemetryApi";
import { apiErrorMessage } from "../services/api";
import { formatTimestamp } from "../utils/datetime";
import { downloadCSV } from "../utils/csv";

export default function Telemetry() {
  const vehicles = usePrimaryVehicle();
  return (
    <div className="resource-page">
      <PageHeader
        title="Telemetry"
        subtitle="The details behind every drive, all in one view."
      />
      {vehicles.isLoading && <Loading />}
      {vehicles.isError ? (
        <EmptyState
          error={apiErrorMessage(vehicles.error)}
          onRetry={() => vehicles.refetch()}
        />
      ) : vehicles.vehicleId ? (
        <TelemetryDetails
          key={vehicles.vehicleId}
          vehicleId={vehicles.vehicleId}
        />
      ) : (
        !vehicles.isLoading && <EmptyState />
      )}
    </div>
  );
}
function TelemetryDetails({ vehicleId }: { vehicleId: number }) {
  const [page, setPage] = useState(0);
  const latest = useLatestTelemetry(vehicleId);
  const history = useQuery({
    queryKey: ["telemetry", "history", vehicleId, "page", page],
    queryFn: () => getTelemetryHistory(vehicleId, page * 20, 20),
  });
  const telemetry = latest.data?.telemetry;
  const metrics = telemetry
    ? [
        ["Speed", `${telemetry.speed.toFixed(1)} km/h`],
        ["Engine speed", `${telemetry.rpm} RPM`],
        ["Fuel level", `${telemetry.fuel_level.toFixed(1)}%`],
        ["Temperature", `${telemetry.engine_temperature.toFixed(1)} °C`],
        ["Battery", `${telemetry.battery_voltage.toFixed(2)} V`],
        ["Oil life", `${telemetry.oil_life.toFixed(1)}%`],
        ["Coolant", `${telemetry.coolant_level.toFixed(1)}%`],
        ["Brake wear", `${telemetry.brake_wear.toFixed(1)}%`],
        ["Front left tire", `${telemetry.tire_pressure_fl.toFixed(1)} PSI`],
        ["Front right tire", `${telemetry.tire_pressure_fr.toFixed(1)} PSI`],
        ["Rear left tire", `${telemetry.tire_pressure_rl.toFixed(1)} PSI`],
        ["Rear right tire", `${telemetry.tire_pressure_rr.toFixed(1)} PSI`],
        ["Engine load", `${telemetry.engine_load.toFixed(1)}%`],
        ["Throttle", `${telemetry.throttle_position.toFixed(1)}%`],
        ["Gear", String(telemetry.gear)],
        [
          "Odometer",
          `${telemetry.odometer.toLocaleString(undefined, { maximumFractionDigits: 2 })} km`,
        ],
      ]
    : [];
  return (
    <>
      <SimulateDrive vehicleId={vehicleId} />
      {latest.isLoading && <Loading />}
      {latest.isError && (
        <p role="alert">
          {apiErrorMessage(latest.error)}{" "}
          <button className="text-button" onClick={() => latest.refetch()}>
            Retry
          </button>
        </p>
      )}
      {telemetry ? (
        <section className="card resource-card">
          <div className="page-toolbar history-heading">
            <h2>Latest sensor readings</h2>
            <span className="report-summary">
              {formatTimestamp(telemetry.timestamp)}
            </span>
          </div>
          <div className="detail-grid">
            {metrics.map(([label, value]) => (
              <div className="metric" key={label}>
                <span>{label}</span>
                <strong>{value}</strong>
              </div>
            ))}
          </div>
        </section>
      ) : (
        !latest.isLoading &&
        !latest.isError && (
          <p className="resource-empty">
            No readings yet. Run a sample drive to bring your telemetry to life.
          </p>
        )
      )}
      <TelemetryCharts vehicleId={vehicleId} />
      <section className="card resource-card">
        <div className="page-toolbar history-heading">
          <h2>Reading history</h2>
          <button
            className="action-button"
            disabled={!history.data?.records.length || history.isFetching}
            onClick={() =>
              downloadCSV(
                `automind-vehicle-${vehicleId}-page-${page + 1}.csv`,
                (history.data?.records ?? []).map((record) => ({ ...record })),
              )
            }
          >
            <Download size={15} />
            Export page CSV
          </button>
        </div>
        {history.isLoading ? (
          <Loading />
        ) : history.isError ? (
          <p role="alert">
            History could not be loaded.{" "}
            <button className="text-button" onClick={() => history.refetch()}>
              Retry
            </button>
          </p>
        ) : !history.data?.records.length ? (
          <p className="resource-empty">No readings on this page.</p>
        ) : (
          <div className="table-scroll">
            <table className="telemetry-table">
              <caption className="sr-only">
                Recorded vehicle telemetry, newest first
              </caption>
              <thead>
                <tr>
                  <th scope="col">Recorded</th>
                  <th scope="col">State</th>
                  <th scope="col">Speed</th>
                  <th scope="col">RPM</th>
                  <th scope="col">Fuel</th>
                  <th scope="col">Temperature</th>
                  <th scope="col">Odometer</th>
                </tr>
              </thead>
              <tbody>
                {history.data.records.map((record) => (
                  <tr key={record.id}>
                    <td>{formatTimestamp(record.timestamp)}</td>
                    <td>
                      {record.vehicle_state.toLowerCase().replaceAll("_", " ")}
                    </td>
                    <td>{record.speed.toFixed(1)} km/h</td>
                    <td>{record.rpm}</td>
                    <td>{record.fuel_level.toFixed(1)}%</td>
                    <td>{record.engine_temperature.toFixed(1)} °C</td>
                    <td>{record.odometer.toFixed(2)} km</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
        <div className="pagination-controls">
          <button
            className="icon-button"
            aria-label="Previous readings page"
            disabled={page === 0 || history.isFetching}
            onClick={() => setPage((value) => value - 1)}
          >
            <ChevronLeft size={16} />
          </button>
          <span>Page {page + 1} · 20 readings per page</span>
          <button
            className="icon-button"
            aria-label="Next readings page"
            disabled={
              history.isFetching || (history.data?.records.length ?? 0) < 20
            }
            onClick={() => setPage((value) => value + 1)}
          >
            <ChevronRight size={16} />
          </button>
        </div>
      </section>
    </>
  );
}
