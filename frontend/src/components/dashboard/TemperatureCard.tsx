import { Thermometer } from "lucide-react";
import Card from "../common/Card";
import Loading from "../common/Loading";
import { useLatestTelemetry } from "../../hooks/useTelemetry";

type Props = { vehicleId: number; };

function TemperatureCard({ vehicleId }: Props) {
  const { data, isLoading, isError } = useLatestTelemetry(vehicleId);

  return (
    <Card className="dashboard-card" animated>
      <div className="dashboard-card__header">
        <h2 className="dashboard-card__title">Temperature</h2>
        <div className="dashboard-card__icon dashboard-card__icon--danger">
          <Thermometer size={20} />
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
          <p className="dashboard-card__value">{data.telemetry.engine_temperature.toFixed(1)}°C</p>
          <p className="dashboard-card__label">Coolant Level: {data.telemetry.coolant_level.toFixed(1)}%</p>
        </div>
      )}
    </Card>
  );
}

export default TemperatureCard;
