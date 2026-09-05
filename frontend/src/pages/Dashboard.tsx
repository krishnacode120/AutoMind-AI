import PageHeader from "../components/common/PageHeader";
import DashboardGrid from "../components/dashboard/DashboardGrid";
import TelemetryCharts from "../components/charts/TelemetryCharts";
import BONChat from "../components/bon/BONChat";
import Loading from "../components/common/Loading";
import { usePrimaryVehicle } from "../hooks/usePrimaryVehicle";
import { Link } from "react-router-dom";
import SimulateDrive from "../components/common/SimulateDrive";

function Dashboard() {
  const { data: vehicles, vehicleId, isLoading, isError } = usePrimaryVehicle();

  return (
    <div className="dashboard-page">
      <PageHeader
        title="Dashboard"
        subtitle="Monitor your vehicle's performance at a glance"
      />

      {isLoading && <Loading />}

      {(isError || (vehicles && vehicles.length === 0)) && (
        <p className="resource-empty">
          {isError ? "Cannot reach the backend." : "No vehicles yet."}{" "}
          <Link to="/vehicles">Manage vehicles</Link>
        </p>
      )}

      {vehicleId && (
        <>
          <SimulateDrive key={vehicleId} vehicleId={vehicleId} />
          <DashboardGrid vehicleId={vehicleId} />
          <TelemetryCharts vehicleId={vehicleId} />
          <BONChat key={vehicleId} vehicleId={vehicleId} />
        </>
      )}
    </div>
  );
}

export default Dashboard;
