export interface Telemetry {
  id: number;
  vehicle_id: number;
  timestamp: string;
  vehicle_state: string;
  driving_mode: string;
  speed: number;
  rpm: number;
  fuel_level: number;
  engine_temperature: number;
  battery_voltage: number;
  oil_life: number;
  coolant_level: number;
  tire_pressure_fl: number;
  tire_pressure_fr: number;
  tire_pressure_rl: number;
  tire_pressure_rr: number;
  brake_wear: number;
  engine_load: number;
  throttle_position: number;
  gear: number;
  trip_distance: number;
  odometer: number;
  fuel_consumption: number;
  created_at: string;
}

export interface LatestTelemetry {
  vehicle_id: number;
  telemetry: Telemetry | null;
}

export interface TelemetryHistory {
  vehicle_id: number;
  records: Telemetry[];
}

