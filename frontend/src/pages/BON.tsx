import PageHeader from "../components/common/PageHeader";
import BONChat from "../components/bon/BONChat";
import Loading from "../components/common/Loading";
import EmptyState from "../components/common/EmptyState";
import { usePrimaryVehicle } from "../hooks/usePrimaryVehicle";
import { apiErrorMessage } from "../services/api";
export default function BON() {
  const query = usePrimaryVehicle();
  return (
    <div className="resource-page">
      <PageHeader
        title="BON"
        subtitle={
          query.vehicle
            ? `Your vehicle assistant, with context from ${query.vehicle.name}.`
            : "A clearer answer to every vehicle question."
        }
      />
      {query.isLoading && <Loading />}
      {query.isError ? (
        <EmptyState
          error={apiErrorMessage(query.error)}
          onRetry={() => query.refetch()}
        />
      ) : query.vehicleId ? (
        <BONChat key={query.vehicleId} vehicleId={query.vehicleId} />
      ) : (
        !query.isLoading && <EmptyState />
      )}
    </div>
  );
}
