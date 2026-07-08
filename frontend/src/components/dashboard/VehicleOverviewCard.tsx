import { Car } from "lucide-react";
import Card from "../common/Card";
import Loading from "../common/Loading";
import { useVehicle } from "../../hooks/useVehicle";

type Props = { vehicleId: number; };

function VehicleOverviewCard({ vehicleId }: Props) {
  const { data: vehicle, isLoading, isError } = useVehicle(vehicleId);

  return (
    <Card className="dashboard-card" animated>
      <div className="dashboard-card__header">
        <h2 className="dashboard-card__title">Vehicle Overview</h2>
        <div className="dashboard-card__icon dashboard-card__icon--primary">
          <Car size={20} />
        </div>
      </div>
      
      {isLoading && <Loading />}
      
      {isError && (
        <p className="dashboard-card__value--sm">Failed to load vehicle.</p>
      )}
      
      {vehicle && (
        <div className="dashboard-card__body">
          <div className="dashboard-card__status">
            <span className="dashboard-card__dot dashboard-card__dot--success" />
            <span className="dashboard-card__label">{vehicle.name}</span>
          </div>
          <div className="vehicle-overview__details">
            <div className="vehicle-overview__detail">
              <span className="vehicle-overview__detail-label">Make / Model</span>
              <span className="vehicle-overview__detail-value">{vehicle.manufacturer} {vehicle.model}</span>
            </div>
            <div className="vehicle-overview__detail">
              <span className="vehicle-overview__detail-label">Year</span>
              <span className="vehicle-overview__detail-value">{vehicle.year}</span>
            </div>
            <div className="vehicle-overview__detail">
              <span className="vehicle-overview__detail-label">Fuel Type</span>
              <span className="vehicle-overview__detail-value">{vehicle.fuel_type}</span>
            </div>
            <div className="vehicle-overview__detail">
              <span className="vehicle-overview__detail-label">Transmission</span>
              <span className="vehicle-overview__detail-value">{vehicle.transmission}</span>
            </div>
          </div>
        </div>
      )}
    </Card>
  );
}

export default VehicleOverviewCard;
