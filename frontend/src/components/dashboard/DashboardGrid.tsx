import AlertsCard from "./AlertsCard";
import BonStatusCard from "./BonStatusCard";
import FuelCard from "./FuelCard";
import HealthCard from "./HealthCard";
import QuickActionsCard from "./QuickActionsCard";
import SpeedCard from "./SpeedCard";
import TemperatureCard from "./TemperatureCard";
import VehicleOverviewCard from "./VehicleOverviewCard";

type DashboardGridProps = {
  vehicleId: number;
};

function DashboardGrid({ vehicleId }: DashboardGridProps) {
  return (
    <div className="dashboard-grid">
      <div className="dashboard-row dashboard-row--2">
        <VehicleOverviewCard vehicleId={vehicleId} />
        <HealthCard vehicleId={vehicleId} />
      </div>
      <div className="dashboard-row dashboard-row--3">
        <SpeedCard vehicleId={vehicleId} />
        <FuelCard vehicleId={vehicleId} />
        <TemperatureCard vehicleId={vehicleId} />
      </div>
      <div className="dashboard-row dashboard-row--3">
        <AlertsCard vehicleId={vehicleId} />
        <BonStatusCard />
        <QuickActionsCard />
      </div>
    </div>
  );
}

export default DashboardGrid;
