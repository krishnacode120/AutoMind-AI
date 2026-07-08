export interface PredictionResult {
  prediction_type: string;
  confidence: number;
  predicted_failure: string;
  recommended_action: string;
  estimated_remaining_km: number | null;
  timestamp: string;
}
