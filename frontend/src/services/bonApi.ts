import api from "./api";

export type BONRequest = {
  vehicle_id: number;
  message: string;
  session_id: string;
};

export type BONResponse = {
  answer: string;
  intent: string;
  confidence: number;
  context_used: Record<string, unknown>;
  timestamp: string;
};

export async function sendMessage(request: BONRequest): Promise<BONResponse> {
  const response = await api.post<BONResponse>("/bon/chat", request);
  return response.data;
}
