export type AlertSeverity = "INFO" | "WARNING" | "CRITICAL";

export type AlertType =
  | "HIGH_ENGINE_TEMP"
  | "LOW_FUEL"
  | "LOW_BATTERY"
  | "LOW_OIL_LIFE"
  | "LOW_COOLANT"
  | "LOW_TIRE_PRESSURE"
  | "HIGH_BRAKE_WEAR"
  | "ENGINE_OVERLOAD"
  | "VEHICLE_HEALTH_CRITICAL";

export interface Alert {
  severity: AlertSeverity;
  type: AlertType;
  title: string;
  description: string;
  recommendation: string;
  timestamp: string;
}

export interface AlertReport {
  alert_count: number;
  highest_severity: AlertSeverity | null;
  alerts: Alert[];
}
