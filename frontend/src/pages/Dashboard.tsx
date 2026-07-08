import PageHeader from "../components/common/PageHeader";
import DashboardGrid from "../components/dashboard/DashboardGrid";
import TelemetryCharts from "../components/charts/TelemetryCharts";
import Loading from "../components/common/Loading";
import { useVehicles } from "../hooks/useVehicle";
import { useTelemetrySocket } from "../hooks/useTelemetrySocket";

function Dashboard() {
  const { data: vehicles, isLoading, isError } = useVehicles();
  const vehicleId = vehicles && vehicles.length > 0 ? vehicles[0].id : null;

  // Initialize WebSocket connection for the selected vehicle
  useTelemetrySocket(vehicleId);

  return (
    <div className="dashboard-page">
      <PageHeader
        title="Dashboard"
        subtitle="Monitor your vehicle's performance at a glance"
      />
      
      {isLoading && <Loading />}
      
      {(isError || (vehicles && vehicles.length === 0)) && (
        <p className="dashboard-card__value--sm">No vehicle available.</p>
      )}

      {vehicleId && (
        <>
          <DashboardGrid vehicleId={vehicleId} />
          <TelemetryCharts vehicleId={vehicleId} />
        </>
      )}
    </div>
  );
}

export default Dashboard;
