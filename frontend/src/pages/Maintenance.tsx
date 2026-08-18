import PageHeader from "../components/common/PageHeader";
import Card from "../components/common/Card";
import Loading from "../components/common/Loading";
import { useMaintenance } from "../hooks/useMaintenance";
import { usePrimaryVehicle } from "../hooks/usePrimaryVehicle";

function Maintenance() {
  const { vehicle, vehicleId, isLoading: vehiclesLoading } = usePrimaryVehicle();
  const { data, isLoading, isError } = useMaintenance(vehicleId ?? 0);

  return (
    <div className="resource-page">
      <PageHeader title="Maintenance" subtitle="Recommended service based on the latest vehicle condition" />
      {(vehiclesLoading || isLoading) && <Loading />}
      {!vehiclesLoading && !vehicle && <Card className="resource-card"><p className="resource-empty">Add a vehicle to review maintenance.</p></Card>}
      {isError && <Card className="resource-card"><p className="resource-empty">Maintenance is unavailable until telemetry is recorded.</p></Card>}
      {data && (
        <Card className="resource-card">
          <p className="report-summary">{data.task_count} recommended tasks <span className={`priority priority--${data.overall_priority.toLowerCase()}`}>{data.overall_priority}</span></p>
          {data.tasks.length ? <div className="data-list">{data.tasks.map((task) => <article className="data-list__item" key={task.id}><div><strong>{task.title}</strong><p>{task.description}</p><p>{task.recommended_action}</p></div><div className="data-list__meta"><span className={`priority priority--${task.priority.toLowerCase()}`}>{task.priority}</span>{task.estimated_km_remaining !== null && <span>{task.estimated_km_remaining.toLocaleString()} km remaining</span>}{task.estimated_days_remaining !== null && <span>{task.estimated_days_remaining} days remaining</span>}</div></article>)}</div> : <p className="resource-empty">No service is currently recommended.</p>}
        </Card>
      )}
    </div>
  );
}

export default Maintenance;
