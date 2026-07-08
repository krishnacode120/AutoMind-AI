import { useQuery } from "@tanstack/react-query";
import { getVehicles, getVehicle } from "../services/vehicleApi";

export function useVehicles() {
  return useQuery({
    queryKey: ["vehicles"],
    queryFn: getVehicles,
  });
}

export function useVehicle(vehicleId: number) {
  return useQuery({
    queryKey: ["vehicles", vehicleId],
    queryFn: () => getVehicle(vehicleId),
    enabled: !!vehicleId,
  });
}
