import PageHeader from "../components/common/PageHeader";
import Card from "../components/common/Card";
import Loading from "../components/common/Loading";
import { useVehicles } from "../hooks/useVehicle";

function Vehicles() {
  const { data: vehicles, isLoading, isError } = useVehicles();

  return (
    <div className="resource-page">
      <PageHeader
        title="Vehicles"
        subtitle="Vehicles currently registered with AutoMind AI"
      />
      <Card className="resource-card">
        {isLoading && <Loading />}
        {isError && <p className="resource-empty">Vehicles are unavailable.</p>}
        {vehicles?.length === 0 && (
          <p className="resource-empty">No vehicles have been added yet.</p>
        )}
        {vehicles && vehicles.length > 0 && (
          <div className="data-list">
            {vehicles.map((vehicle) => (
              <article className="data-list__item" key={vehicle.id}>
                <div>
                  <strong>{vehicle.name}</strong>
                  <p>{vehicle.manufacturer} {vehicle.model}</p>
                </div>
                <div className="data-list__meta">
                  <span>{vehicle.year}</span>
                  <span>{vehicle.fuel_type}</span>
                  <span>{vehicle.odometer.toLocaleString()} km</span>
                </div>
              </article>
            ))}
          </div>
        )}
      </Card>
    </div>
  );
}

export default Vehicles;
