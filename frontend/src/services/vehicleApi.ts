import api from "./api";
import type { ApiResponse } from "../types/common";
import type { Vehicle, VehicleCreate } from "../types/vehicle";

export async function getVehicles(): Promise<Vehicle[]> {
  const vehicles: Vehicle[] = [];
  for (let skip = 0; ; skip += 1000) {
    const response = await api.get<ApiResponse<Vehicle[]>>("/vehicles", {
      params: { skip, limit: 1000 },
    });
    vehicles.push(...response.data.data);
    if (response.data.data.length < 1000) return vehicles;
  }
}

export async function getVehicle(vehicleId: number): Promise<Vehicle> {
  const response = await api.get<ApiResponse<Vehicle>>(
    `/vehicles/${vehicleId}`,
  );
  return response.data.data;
}

export async function saveVehicle(
  data: VehicleCreate,
  id?: number,
): Promise<Vehicle> {
  const response = id
    ? await api.put<ApiResponse<Vehicle>>(`/vehicles/${id}`, data)
    : await api.post<ApiResponse<Vehicle>>("/vehicles", data);
  return response.data.data;
}

export async function deleteVehicle(id: number): Promise<void> {
  await api.delete(`/vehicles/${id}`);
}
