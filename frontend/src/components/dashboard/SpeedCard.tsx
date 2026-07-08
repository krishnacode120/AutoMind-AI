import { Gauge } from "lucide-react";
import Card from "../common/Card";
import Loading from "../common/Loading";
import { useLatestTelemetry } from "../../hooks/useTelemetry";

type Props = { vehicleId: number; };

function SpeedCard({ vehicleId }: Props) {
  const { data, isLoading, isError } = useLatestTelemetry(vehicleId);

  return (
    <Card className="dashboard-card" animated>
      <div className="dashboard-card__header">
        <h2 className="dashboard-card__title">Speed & RPM</h2>
        <div className="dashboard-card__icon dashboard-card__icon--primary">
          <Gauge size={20} />
        </div>
      </div>
      
      {isLoading && <Loading />}
      
      {isError && (
        <p className="dashboard-card__value--sm">Failed to load telemetry.</p>
      )}

      {data && !data.telemetry && !isLoading && !isError && (
        <p className="dashboard-card__value--sm">No telemetry available.</p>
      )}

      {data?.telemetry && (
        <div className="dashboard-card__body">
          <p className="dashboard-card__value">{data.telemetry.speed.toFixed(0)} km/h</p>
          <div className="vehicle-overview__details" style={{ marginTop: '12px' }}>
             <div className="vehicle-overview__detail">
              <span className="vehicle-overview__detail-label">Gear</span>
              <span className="vehicle-overview__detail-value">{data.telemetry.gear}</span>
            </div>
            <div className="vehicle-overview__detail">
              <span className="vehicle-overview__detail-label">RPM</span>
              <span className="vehicle-overview__detail-value">{data.telemetry.rpm.toFixed(0)}</span>
            </div>
          </div>
        </div>
      )}
    </Card>
  );
}

export default SpeedCard;
