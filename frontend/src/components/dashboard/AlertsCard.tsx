import { AlertTriangle, ShieldCheck } from "lucide-react";
import Card from "../common/Card";
import Loading from "../common/Loading";
import { useAlerts } from "../../hooks/useAlerts";

type Props = { vehicleId: number; };

function AlertsCard({ vehicleId }: Props) {
  const { data, isLoading, isError } = useAlerts(vehicleId);

  return (
    <Card className="dashboard-card" animated>
      <div className="dashboard-card__header">
        <h2 className="dashboard-card__title">Alerts</h2>
        <div className="dashboard-card__icon dashboard-card__icon--warning">
          <AlertTriangle size={20} />
        </div>
      </div>
      
      {isLoading && <Loading />}
      
      {/* TODO: Alerts endpoint is not yet implemented in backend */}
      {isError && (
        <p className="dashboard-card__value--sm">Alerts unavailable.</p>
      )}

      {data && data.alert_count === 0 && (
        <div className="dashboard-card__body">
          <div className="alerts-card__list">
            <div className="alerts-card__item">
              <ShieldCheck size={16} className="alerts-card__item-icon" />
              <span>No active alerts</span>
            </div>
          </div>
        </div>
      )}

      {data && data.alert_count > 0 && (
        <div className="dashboard-card__body">
          <div className="dashboard-card__status" style={{ marginBottom: "8px" }}>
            <span className="dashboard-card__dot dashboard-card__dot--primary" />
            <span className="dashboard-card__label">
              {data.alert_count} Alerts (Max: {data.highest_severity})
            </span>
          </div>
          <div className="alerts-card__list">
            {data.alerts.slice(0, 3).map((alert, index) => (
              <div key={index} className="alerts-card__item">
                <AlertTriangle size={16} className="dashboard-card__icon--warning" style={{ background: 'none' }} />
                <span>{alert.title}</span>
              </div>
            ))}
          </div>
        </div>
      )}
    </Card>
  );
}

export default AlertsCard;
