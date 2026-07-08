import { useTelemetryHistory } from "../../hooks/useTelemetry";
import Loading from "../common/Loading";
import Card from "../common/Card";
import SpeedChart from "./SpeedChart";
import RPMChart from "./RPMChart";
import TemperatureChart from "./TemperatureChart";
import FuelChart from "./FuelChart";

type Props = {
  vehicleId: number;
};

function TelemetryCharts({ vehicleId }: Props) {
  const { data, isLoading, isError } = useTelemetryHistory(vehicleId);

  if (isLoading) {
    return (
      <Card className="dashboard-card">
        <Loading />
      </Card>
    );
  }

  // TODO: Implement history endpoint data fallback securely. Currently backend might not have it ready.
  if (isError || !data || data.records.length === 0) {
    return (
      <Card className="dashboard-card">
        <p className="dashboard-card__value--sm">No telemetry history available.</p>
      </Card>
    );
  }

  const { records } = data;

  return (
    <div className="dashboard-row dashboard-row--2" style={{ marginTop: "24px" }}>
      <SpeedChart data={records} />
      <RPMChart data={records} />
      <TemperatureChart data={records} />
      <FuelChart data={records} />
    </div>
  );
}

export default TelemetryCharts;
