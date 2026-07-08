import api from "./api";
import type { ApiResponse } from "../types/common";
import type { Vehicle } from "../types/vehicle";

export async function getVehicles(): Promise<Vehicle[]> {
  const response = await api.get<ApiResponse<Vehicle[]>>("/vehicles");
  return response.data.data;
}

export async function getVehicle(vehicleId: number): Promise<Vehicle> {
  const response = await api.get<ApiResponse<Vehicle>>(`/vehicles/${vehicleId}`);
  return response.data.data;
}
