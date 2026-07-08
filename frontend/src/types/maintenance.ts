export type MaintenancePriority = "LOW" | "MEDIUM" | "HIGH" | "URGENT";

export interface MaintenanceTask {
  id: string;
  title: string;
  description: string;
  priority: MaintenancePriority;
  estimated_km_remaining: number | null;
  estimated_days_remaining: number | null;
  recommended_action: string;
  component: string;
}

export interface MaintenanceReport {
  overall_priority: MaintenancePriority;
  task_count: number;
  tasks: MaintenanceTask[];
  timestamp: string;
}
