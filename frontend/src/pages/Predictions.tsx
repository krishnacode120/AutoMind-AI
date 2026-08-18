import PageHeader from "../components/common/PageHeader";
import Card from "../components/common/Card";
import Loading from "../components/common/Loading";
import { usePrediction } from "../hooks/usePrediction";
import { usePrimaryVehicle } from "../hooks/usePrimaryVehicle";

function Predictions() {
  const { vehicle, vehicleId, isLoading: vehiclesLoading } = usePrimaryVehicle();
  const { data, isLoading, isError } = usePrediction(vehicleId ?? 0);

  return (
    <div className="resource-page">
      <PageHeader title="Predictions" subtitle="Failure risk from the current vehicle condition" />
      {(vehiclesLoading || isLoading) && <Loading />}
      {!vehiclesLoading && !vehicle && <Card className="resource-card"><p className="resource-empty">Add a vehicle to review prediction results.</p></Card>}
      {isError && <Card className="resource-card"><p className="resource-empty">Prediction is unavailable until telemetry is recorded.</p></Card>}
      {data && (
        <Card className="resource-card">
          <div className="detail-grid">
            <Metric label="Assessment" value={data.predicted_failure} />
            <Metric label="Confidence" value={`${Math.round(data.confidence * 100)}%`} />
            <Metric label="Model" value={data.prediction_type} />
            <Metric label="Estimated remaining" value={data.estimated_remaining_km === null ? "Not available" : `${data.estimated_remaining_km.toLocaleString()} km`} />
          </div>
          <section className="report-section"><h2>Recommended action</h2><p>{data.recommended_action}</p></section>
        </Card>
      )}
    </div>
  );
}

function Metric({ label, value }: { label: string; value: string }) {
  return <div className="metric"><span>{label}</span><strong>{value}</strong></div>;
}

export default Predictions;
