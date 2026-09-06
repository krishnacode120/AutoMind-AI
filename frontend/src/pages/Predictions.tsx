import VehicleWorkspace from "../components/common/VehicleWorkspace";
import Loading from "../components/common/Loading";
import { usePrimaryVehicle } from "../hooks/usePrimaryVehicle";
import { useInsights } from "../hooks/useInsights";
export default function Predictions() {
  const { vehicleId } = usePrimaryVehicle();
  const query = useInsights(vehicleId ?? 0);
  const data = query.data?.prediction;
  return (
    <VehicleWorkspace
      title="Predictions"
      subtitle="Look ahead with a clearer view of your vehicle’s condition."
    >
      {query.isLoading && <Loading />}
      {query.isError && (
        <p role="alert">
          Predictions could not be loaded.{" "}
          <button className="text-button" onClick={() => query.refetch()}>
            Retry
          </button>
        </p>
      )}
      {data && (
        <>
          <section className="card resource-card prediction-overview">
            <p className="eyebrow">CURRENT ASSESSMENT</p>
            <h2>{data.predicted_failure.replaceAll("_", " ")}</h2>
            <div className="detail-grid">
              <div className="metric">
                <span>Model confidence</span>
                <strong>{Math.round(data.confidence * 100)}%</strong>
              </div>
              <div className="metric">
                <span>Prediction method</span>
                <strong>{data.prediction_type}</strong>
              </div>
              <div className="metric">
                <span>Estimated remaining</span>
                <strong>
                  {data.estimated_remaining_km === null
                    ? "Not available"
                    : `${data.estimated_remaining_km.toLocaleString()} km`}
                </strong>
              </div>
            </div>
          </section>
          <section className="card resource-card">
            <h2>Recommended next step</h2>
            <p className="report-summary">{data.recommended_action}</p>
          </section>
          <p className="method-note">
            These estimates use rules or a model trained on synthetic data.
            Confidence describes the model output; it is not a measured
            probability of a real-world failure.
          </p>
        </>
      )}
    </VehicleWorkspace>
  );
}
