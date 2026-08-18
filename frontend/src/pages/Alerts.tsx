import PageHeader from "../components/common/PageHeader";
import Card from "../components/common/Card";
import Loading from "../components/common/Loading";
import { useAlerts } from "../hooks/useAlerts";
import { usePrimaryVehicle } from "../hooks/usePrimaryVehicle";

function Alerts() {
  const { vehicle, vehicleId, isLoading: vehiclesLoading } = usePrimaryVehicle();
  const { data, isLoading, isError } = useAlerts(vehicleId ?? 0);

  return (
    <div className="resource-page">
      <PageHeader title="Alerts" subtitle="Active conditions that need attention" />
      {(vehiclesLoading || isLoading) && <Loading />}
      {!vehiclesLoading && !vehicle && <Card className="resource-card"><p className="resource-empty">Add a vehicle to review alerts.</p></Card>}
      {isError && <Card className="resource-card"><p className="resource-empty">Alerts are unavailable until telemetry is recorded.</p></Card>}
      {data && (
        <Card className="resource-card">
          <p className="report-summary">{data.alert_count} active alerts{data.highest_severity ? ` | Highest severity: ${data.highest_severity}` : ""}</p>
          {data.alerts.length ? <div className="data-list">{data.alerts.map((alert) => <article className="data-list__item" key={`${alert.type}-${alert.timestamp}`}><div><strong>{alert.title}</strong><p>{alert.description}</p><p>{alert.recommendation}</p></div><span className={`priority priority--${alert.severity.toLowerCase()}`}>{alert.severity}</span></article>)}</div> : <p className="resource-empty">No active alerts.</p>}
        </Card>
      )}
    </div>
  );
}

export default Alerts;
