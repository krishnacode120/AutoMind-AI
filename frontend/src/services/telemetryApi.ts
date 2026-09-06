import api from "./api";
import type { ApiResponse } from "../types/common";
import type { LatestTelemetry, TelemetryHistory } from "../types/telemetry";

export async function getLatestTelemetry(
  vehicleId: number,
): Promise<LatestTelemetry> {
  const response = await api.get<ApiResponse<LatestTelemetry>>(
    `/telemetry/latest/${vehicleId}`,
  );
  return response.data.data;
}

export async function getTelemetryHistory(
  vehicleId: number,
  skip = 0,
  limit = 100,
): Promise<TelemetryHistory> {
  const response = await api.get<ApiResponse<TelemetryHistory>>(
    `/telemetry/history/${vehicleId}`,
    { params: { skip, limit } },
  );
  return response.data.data;
}
