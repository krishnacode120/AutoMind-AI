import type { ReactNode } from "react";
import PageHeader from "./PageHeader";
import EmptyState from "./EmptyState";
import Loading from "./Loading";
import SimulateDrive from "./SimulateDrive";
import { usePrimaryVehicle } from "../../hooks/usePrimaryVehicle";
import { useLatestTelemetry } from "../../hooks/useTelemetry";
import { apiErrorMessage } from "../../services/api";

export default function VehicleWorkspace({
  title,
  subtitle,
  children,
}: {
  title: string;
  subtitle: string;
  children: ReactNode;
}) {
  const vehicles = usePrimaryVehicle();
  const latest = useLatestTelemetry(vehicles.vehicleId ?? 0);
  return (
    <div className="resource-page">
      <PageHeader title={title} subtitle={subtitle} />
      {vehicles.isLoading ? (
        <Loading />
      ) : vehicles.isError ? (
        <EmptyState
          error={apiErrorMessage(vehicles.error)}
          onRetry={() => vehicles.refetch()}
        />
      ) : !vehicles.vehicle ? (
        <EmptyState />
      ) : latest.isLoading ? (
        <Loading />
      ) : latest.isError ? (
        <EmptyState
          error={apiErrorMessage(latest.error)}
          onRetry={() => latest.refetch()}
        />
      ) : !latest.data?.telemetry ? (
        <>
          <section className="card resource-card">
            <h2>Give your insights a starting point.</h2>
            <p className="resource-empty">
              There are no readings for {vehicles.vehicle.name} yet. Run a
              sample drive to generate your first report.
            </p>
          </section>
          <SimulateDrive
            key={vehicles.vehicleId}
            vehicleId={vehicles.vehicleId!}
          />
        </>
      ) : (
        children
      )}
    </div>
  );
}
