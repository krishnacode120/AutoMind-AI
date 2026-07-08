import { Fuel } from "lucide-react";
import Card from "../common/Card";
import Loading from "../common/Loading";
import { useLatestTelemetry } from "../../hooks/useTelemetry";

type Props = { vehicleId: number; };

function FuelCard({ vehicleId }: Props) {
  const { data, isLoading, isError } = useLatestTelemetry(vehicleId);

  return (
    <Card className="dashboard-card" animated>
      <div className="dashboard-card__header">
        <h2 className="dashboard-card__title">Fuel & Battery</h2>
        <div className="dashboard-card__icon dashboard-card__icon--warning">
          <Fuel size={20} />
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
          <p className="dashboard-card__value">{data.telemetry.fuel_level.toFixed(1)}%</p>
          <p className="dashboard-card__label">Battery: {data.telemetry.battery_voltage.toFixed(1)}V</p>
        </div>
      )}
    </Card>
  );
}

export default FuelCard;
