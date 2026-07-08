import { useQuery } from "@tanstack/react-query";
import { getPrediction } from "../services/predictionApi";

export function usePrediction(vehicleId: number) {
  return useQuery({
    queryKey: ["prediction", vehicleId],
    queryFn: () => getPrediction(vehicleId),
    enabled: !!vehicleId,
  });
}
