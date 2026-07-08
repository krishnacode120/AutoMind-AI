import api from "./api";
import type { ApiResponse } from "../types/common";
import type { AlertReport } from "../types/alert";

export async function getAlerts(vehicleId: number): Promise<AlertReport> {
  const response = await api.get<ApiResponse<AlertReport>>(`/vehicles/${vehicleId}/alerts`);
  return response.data.data;
}
