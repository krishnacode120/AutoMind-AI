import { HeartPulse } from "lucide-react";
import Card from "../common/Card";
import Loading from "../common/Loading";
import { useHealth } from "../../hooks/useHealth";

type Props = { vehicleId: number; };

function HealthCard({ vehicleId }: Props) {
  const { data, isLoading, isError } = useHealth(vehicleId);

  return (
    <Card className="dashboard-card" animated>
      <div className="dashboard-card__header">
        <h2 className="dashboard-card__title">Health</h2>
        <div className="dashboard-card__icon dashboard-card__icon--success">
          <HeartPulse size={20} />
        </div>
      </div>
      
      {isLoading && <Loading />}
      
      {/* TODO: Health endpoint is not yet implemented in backend */}
      {isError && (
        <p className="dashboard-card__value--sm">Health data unavailable.</p>
      )}

      {data && (
        <>
          <div className="dashboard-card__body">
            <p className="dashboard-card__value">{data.health_score}%</p>
            <p className="dashboard-card__label">{data.health_status}</p>
          </div>
          <div className="health-card__bar-track">
            <div 
              className="health-card__bar-fill" 
              style={{ width: `${data.health_score}%` }}
            />
          </div>
        </>
      )}
    </Card>
  );
}

export default HealthCard;
