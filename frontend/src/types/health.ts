export interface HealthReport {
  health_score: number;
  health_status: string;
  penalties: Record<string, number>;
  recommendations: string[];
  timestamp: string;
}
