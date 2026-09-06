import VehicleWorkspace from "../components/common/VehicleWorkspace";
import Loading from "../components/common/Loading";
import { usePrimaryVehicle } from "../hooks/usePrimaryVehicle";
import { useInsights } from "../hooks/useInsights";

export default function Health() {
  const { vehicleId } = usePrimaryVehicle();
  const query = useInsights(vehicleId ?? 0);
  const data = query.data?.health;
  return (
    <VehicleWorkspace
      title="Health"
      subtitle="Understand the condition of every essential system."
    >
      {query.isLoading && <Loading />}
      {query.isError && (
        <p role="alert">
          Health could not be loaded.{" "}
          <button className="text-button" onClick={() => query.refetch()}>
            Retry
          </button>
        </p>
      )}
      {data && (
        <>
          <section className="card resource-card">
            <div className="health-summary">
              <strong>
                {data.health_score}
                <small>/100</small>
              </strong>
              <span className="health-status">{data.health_status}</span>
            </div>
            <div className="health-card__bar-track">
              <div
                className="health-card__bar-fill"
                style={{
                  width: `${data.health_score}%`,
                  background:
                    data.health_score < 75
                      ? "var(--color-warning)"
                      : "var(--color-success)",
                }}
              />
            </div>
            <p className="report-summary">
              A rule-based assessment of the latest reading, across seven
              vehicle systems.
            </p>
          </section>
          <div className="system-grid">
            {Object.entries(data.penalties).map(([name, penalty]) => (
              <section className="system-card card" key={name}>
                <span
                  className={"status-dot " + (penalty > 0 ? "warning-dot" : "")}
                />
                <h2>{name.replaceAll("_", " ")}</h2>
                <strong>
                  {penalty > 0 ? "Needs attention" : "Within range"}
                </strong>
                <span>
                  {penalty > 0
                    ? `−${penalty} health points`
                    : "No health penalty"}
                </span>
              </section>
            ))}
          </div>
          <section className="card resource-card">
            <h2>Recommended next steps</h2>
            {data.recommendations.length ? (
              <ul className="report-list">
                {data.recommendations.map((item) => (
                  <li key={item}>{item}</li>
                ))}
              </ul>
            ) : (
              <p className="resource-empty">
                No immediate actions suggested by the latest reading.
              </p>
            )}
          </section>
        </>
      )}
    </VehicleWorkspace>
  );
}
