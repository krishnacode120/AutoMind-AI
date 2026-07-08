import api from "./api";
import type { ApiResponse } from "../types/common";
import type { HealthReport } from "../types/health";

export async function getHealth(vehicleId: number): Promise<HealthReport> {
  const response = await api.get<ApiResponse<HealthReport>>(`/vehicles/${vehicleId}/health`);
  return response.data.data;
}
