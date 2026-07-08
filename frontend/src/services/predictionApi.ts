import api from "./api";
import type { ApiResponse } from "../types/common";
import type { PredictionResult } from "../types/prediction";

export async function getPrediction(vehicleId: number): Promise<PredictionResult> {
  const response = await api.get<ApiResponse<PredictionResult>>(`/vehicles/${vehicleId}/prediction`);
  return response.data.data;
}
