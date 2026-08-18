import { useVehicles } from "./useVehicle";

export function usePrimaryVehicle() {
  const vehiclesQuery = useVehicles();
  const vehicle = vehiclesQuery.data?.[0] ?? null;

  return {
    ...vehiclesQuery,
    vehicle,
    vehicleId: vehicle?.id ?? null,
  };
}
