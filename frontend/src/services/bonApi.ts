import api from "./api";
import axios from "axios";

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

export async function sendMessage(
  request: BONRequest,
  signal?: AbortSignal,
): Promise<BONResponse> {
  const response = await api.post<BONResponse>("/bon/chat", request, {
    signal,
  });
  return response.data;
}

export async function clearSession(sessionId: string): Promise<void> {
  try {
    await api.delete(`/bon/sessions/${encodeURIComponent(sessionId)}`);
  } catch (error) {
    if (!axios.isAxiosError(error) || error.response?.status !== 404)
      throw error;
  }
}
