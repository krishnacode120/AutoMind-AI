import { useQuery } from "@tanstack/react-query";
import { getAlerts } from "../services/alertApi";

export function useAlerts(vehicleId: number) {
  return useQuery({
    queryKey: ["alerts", vehicleId],
    queryFn: () => getAlerts(vehicleId),
    enabled: !!vehicleId,
  });
}
