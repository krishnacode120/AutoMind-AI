import { ArrowRight, CarFront, RefreshCw, WifiOff } from "lucide-react";
import { Link } from "react-router-dom";
export default function EmptyState({
  error,
  onRetry,
}: {
  error?: string;
  onRetry?: () => void;
}) {
  return (
    <section className="empty-state card">
      <span className="empty-state-icon">
        {error ? <WifiOff size={30} /> : <CarFront size={34} />}
      </span>
      <p className="eyebrow">
        {error ? "CONNECTION INTERRUPTED" : "YOUR WORKSPACE STARTS HERE"}
      </p>
      <h2>
        {error
          ? "Let’s get you reconnected"
          : "Every journey starts with a vehicle."}
      </h2>
      <p>
        {error ||
          "Add your first vehicle, simulate a drive, and explore its health, telemetry, and maintenance insights in one place."}
      </p>
      {error ? (
        <button className="action-button primary" onClick={onRetry}>
          <RefreshCw size={16} />
          Try again
        </button>
      ) : (
        <Link className="action-button primary" to="/vehicles">
          Add your first vehicle <ArrowRight size={16} />
        </Link>
      )}
    </section>
  );
}
