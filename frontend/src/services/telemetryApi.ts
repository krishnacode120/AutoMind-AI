import api from "./api";
import type { ApiResponse } from "../types/common";
import type { LatestTelemetry, TelemetryHistory } from "../types/telemetry";

export async function getLatestTelemetry(vehicleId: number): Promise<LatestTelemetry> {
  const response = await api.get<ApiResponse<LatestTelemetry>>(`/telemetry/latest/${vehicleId}`);
  return response.data.data;
}

export async function getTelemetryHistory(vehicleId: number): Promise<TelemetryHistory> {
  const response = await api.get<ApiResponse<TelemetryHistory>>(`/telemetry/history/${vehicleId}`);
  return response.data.data;
}

