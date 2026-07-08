import api from "./api";
import type { ApiResponse } from "../types/common";
import type { MaintenanceReport } from "../types/maintenance";

export async function getMaintenance(vehicleId: number): Promise<MaintenanceReport> {
  const response = await api.get<ApiResponse<MaintenanceReport>>(`/vehicles/${vehicleId}/maintenance`);
  return response.data.data;
}
