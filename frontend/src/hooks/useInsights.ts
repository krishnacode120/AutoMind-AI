import { useQuery } from "@tanstack/react-query";
import api from "../services/api";
import { useLatestTelemetry } from "./useTelemetry";
import type { ApiResponse } from "../types/common";
import type { HealthReport } from "../types/health";
import type { AlertReport } from "../types/alert";
import type { MaintenanceReport } from "../types/maintenance";
import type { PredictionResult } from "../types/prediction";

export interface VehicleInsights {
  health: HealthReport;
  alerts: AlertReport;
  maintenance: MaintenanceReport;
  prediction: PredictionResult;
}
export function useInsights(vehicleId: number) {
  const latest = useLatestTelemetry(vehicleId);
  return useQuery({
    queryKey: ["insights", vehicleId],
    queryFn: async () =>
      (
        await api.get<ApiResponse<VehicleInsights>>(
          `/vehicles/${vehicleId}/insights`,
        )
      ).data.data,
    enabled: !!vehicleId && !!latest.data?.telemetry,
  });
}
