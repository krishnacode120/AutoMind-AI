export interface Vehicle {
  id: number;
  uuid: string;
  name: string;
  manufacturer: string;
  model: string;
  year: number;
  fuel_type: string;
  transmission: string;
  odometer: number;
  created_at: string;
  updated_at: string;
}

export interface VehicleCreate {
  name: string;
  manufacturer: string;
  model: string;
  year: number;
  fuel_type: string;
  transmission: string;
  odometer?: number;
}
