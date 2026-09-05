import PageHeader from "../components/common/PageHeader";
import BONChat from "../components/bon/BONChat";
import Loading from "../components/common/Loading";
import { usePrimaryVehicle } from "../hooks/usePrimaryVehicle";
import { Link } from "react-router-dom";

function BON() {
  const { vehicleId, isLoading, isError } = usePrimaryVehicle();
  return (
    <div className="resource-page">
      <PageHeader title="BON" />
      {isLoading && <Loading />}
      {isError && (
        <p role="alert">Vehicle data is unavailable. Check your connection.</p>
      )}
      {!isLoading && !isError && !vehicleId && (
        <p>
          <Link to="/vehicles">Add a vehicle</Link> to start a conversation.
        </p>
      )}
      {vehicleId && <BONChat key={vehicleId} vehicleId={vehicleId} />}
    </div>
  );
}

export default BON;
