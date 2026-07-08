import { useQuery } from "@tanstack/react-query";
import { getHealth } from "../services/healthApi";

export function useHealth(vehicleId: number) {
  return useQuery({
    queryKey: ["health", vehicleId],
    queryFn: () => getHealth(vehicleId),
    enabled: !!vehicleId,
  });
}
