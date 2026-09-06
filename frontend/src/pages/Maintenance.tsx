import { Wrench } from "lucide-react";
import VehicleWorkspace from "../components/common/VehicleWorkspace";
import Loading from "../components/common/Loading";
import { usePrimaryVehicle } from "../hooks/usePrimaryVehicle";
import { useInsights } from "../hooks/useInsights";
export default function Maintenance() {
  const { vehicleId } = usePrimaryVehicle();
  const query = useInsights(vehicleId ?? 0);
  const data = query.data?.maintenance;
  return (
    <VehicleWorkspace
      title="Maintenance"
      subtitle="Keep small issues from becoming bigger interruptions."
    >
      {query.isLoading && <Loading />}
      {query.isError && (
        <p role="alert">
          Maintenance could not be loaded.{" "}
          <button className="text-button" onClick={() => query.refetch()}>
            Retry
          </button>
        </p>
      )}
      {data && (
        <>
          <p className="report-summary">
            {data.task_count} recommended tasks · Suggested from the latest
            vehicle condition
          </p>
          {data.tasks.length ? (
            <div className="data-list">
              {data.tasks.map((task) => (
                <article className="data-list__item" key={task.id}>
                  <div>
                    <span
                      className={`priority priority--${task.priority.toLowerCase()}`}
                    >
                      {task.priority}
                    </span>
                    <h2>{task.title}</h2>
                    <p>{task.description}</p>
                    <p className="recommended-action">
                      {task.recommended_action}
                    </p>
                  </div>
                  <div className="data-list__meta">
                    <strong>{task.component}</strong>
                    {task.estimated_km_remaining !== null && (
                      <span>
                        Within {task.estimated_km_remaining.toLocaleString()} km
                      </span>
                    )}
                    {task.estimated_days_remaining !== null && (
                      <span>Within {task.estimated_days_remaining} days</span>
                    )}
                  </div>
                </article>
              ))}
            </div>
          ) : (
            <section className="card all-clear">
              <Wrench size={34} />
              <h2>Nothing due right now.</h2>
              <p>
                Continue your usual service schedule. New recommendations will
                appear as conditions change.
              </p>
            </section>
          )}
        </>
      )}
    </VehicleWorkspace>
  );
}
