import axios from "axios";

export const API_BASE_URL = (
  import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000/api/v1"
).replace(/\/$/, "");

const api = axios.create({ baseURL: API_BASE_URL, timeout: 15000 });

export function apiErrorMessage(error: unknown): string {
  if (axios.isAxiosError(error)) {
    const body = error.response?.data;
    if (typeof body?.message === "string") return body.message;
    if (typeof body?.detail === "string") return body.detail;
    if (Array.isArray(body?.detail)) {
      return body.detail.map((item: { msg: string }) => item.msg).join(". ");
    }
  }
  return "Unable to complete the request. Check your connection and try again.";
}

export default api;
