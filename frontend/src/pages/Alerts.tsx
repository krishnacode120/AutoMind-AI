import { useState } from "react";
import { CheckCircle2 } from "lucide-react";
import VehicleWorkspace from "../components/common/VehicleWorkspace";
import Loading from "../components/common/Loading";
import { usePrimaryVehicle } from "../hooks/usePrimaryVehicle";
import { useInsights } from "../hooks/useInsights";

export default function Alerts() {
  const { vehicleId } = usePrimaryVehicle();
  const query = useInsights(vehicleId ?? 0);
  const [filter, setFilter] = useState("ALL");
  const alerts = query.data?.alerts.alerts ?? [];
  const filtered = alerts.filter(
    (alert) => filter === "ALL" || alert.severity === filter,
  );
  return (
    <VehicleWorkspace
      title="Alerts"
      subtitle="Spot the signals that need your attention."
    >
      {query.isLoading && <Loading />}
      {query.isError && (
        <p role="alert">
          Alerts could not be loaded.{" "}
          <button className="text-button" onClick={() => query.refetch()}>
            Retry
          </button>
        </p>
      )}
      {query.data && (
        <>
          <div className="page-toolbar">
            <p className="report-summary">
              {alerts.length} active {alerts.length === 1 ? "alert" : "alerts"}{" "}
              from the latest reading
            </p>
            <div className="chart-tabs" aria-label="Alert severity">
              {["ALL", "CRITICAL", "WARNING", "INFO"].map((level) => (
                <button
                  key={level}
                  aria-pressed={filter === level}
                  onClick={() => setFilter(level)}
                >
                  {level.toLowerCase()}
                </button>
              ))}
            </div>
          </div>
          {filtered.length ? (
            <div className="data-list">
              {filtered.map((alert) => (
                <article
                  className="data-list__item alert-detail"
                  key={alert.type}
                >
                  <div>
                    <span
                      className={`priority priority--${alert.severity.toLowerCase()}`}
                    >
                      {alert.severity}
                    </span>
                    <h2>{alert.title}</h2>
                    <p>{alert.description}</p>
                    <p className="recommended-action">{alert.recommendation}</p>
                  </div>
                </article>
              ))}
            </div>
          ) : (
            <section className="card all-clear">
              <CheckCircle2 size={36} />
              <h2>
                {alerts.length
                  ? "No alerts in this category."
                  : "All clear for now."}
              </h2>
              <p>
                Alerts reflect the current reading and update as new telemetry
                arrives.
              </p>
            </section>
          )}
        </>
      )}
    </VehicleWorkspace>
  );
}
