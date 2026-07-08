import { useQuery } from "@tanstack/react-query";
import { getMaintenance } from "../services/maintenanceApi";

export function useMaintenance(vehicleId: number) {
  return useQuery({
    queryKey: ["maintenance", vehicleId],
    queryFn: () => getMaintenance(vehicleId),
    enabled: !!vehicleId,
  });
}
