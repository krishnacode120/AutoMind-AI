import { useQuery } from "@tanstack/react-query";
import { getLatestTelemetry, getTelemetryHistory } from "../services/telemetryApi";

export function useLatestTelemetry(vehicleId: number) {
  return useQuery({
    queryKey: ["telemetry", "latest", vehicleId],
    queryFn: () => getLatestTelemetry(vehicleId),
    enabled: !!vehicleId,
  });
}

export function useTelemetryHistory(vehicleId: number) {
  return useQuery({
    queryKey: ["telemetry", "history", vehicleId],
    queryFn: () => getTelemetryHistory(vehicleId),
    enabled: !!vehicleId,
  });
}

