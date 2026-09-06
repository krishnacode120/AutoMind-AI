import { ConnectionState, TelemetrySocketMessage } from "./types";
import { EventEmitter } from "./events";
import { API_BASE_URL } from "../api";

const RECONNECT_DELAYS = [1000, 2000, 4000, 8000, 30000]; // Defined backoff delays

export class TelemetryWebSocketClient extends EventEmitter {
  private socket: WebSocket | null = null;
  private url: string;
  private state: ConnectionState = ConnectionState.DISCONNECTED;
  private reconnectAttempts = 0;
  private reconnectTimeoutId: ReturnType<typeof setTimeout> | null = null;

  constructor(vehicleId: number) {
    super();
    const base = new URL(
      import.meta.env.VITE_WS_BASE_URL || API_BASE_URL,
      window.location.origin,
    );
    base.protocol =
      base.protocol === "https:" || base.protocol === "wss:" ? "wss:" : "ws:";
    this.url = `${base.toString().replace(/\/$/, "")}/ws/telemetry/${vehicleId}`;
  }

  public connect() {
    if (
      this.socket &&
      (this.socket.readyState === WebSocket.OPEN ||
        this.socket.readyState === WebSocket.CONNECTING)
    ) {
      return;
    }

    this.setState(
      this.reconnectAttempts === 0
        ? ConnectionState.CONNECTING
        : ConnectionState.RECONNECTING,
    );

    this.socket = new WebSocket(this.url);

    this.socket.onopen = () => {
      this.reconnectAttempts = 0;
      this.setState(ConnectionState.CONNECTED);
    };

    this.socket.onmessage = (event) => {
      try {
        const message: TelemetrySocketMessage = JSON.parse(event.data);
        this.emit("message", message);
      } catch (err) {
        console.error("WebSocket message parsing error:", err);
      }
    };

    this.socket.onclose = () => {
      this.socket = null;
      if (this.state !== ConnectionState.DISCONNECTED) {
        this.handleReconnect();
      }
    };

    this.socket.onerror = (error) => {
      this.setState(ConnectionState.ERROR);
      this.emit("error", error);
    };
  }

  public disconnect() {
    this.setState(ConnectionState.DISCONNECTED);
    if (this.reconnectTimeoutId) {
      clearTimeout(this.reconnectTimeoutId);
      this.reconnectTimeoutId = null;
    }
    if (this.socket) {
      this.socket.onclose = null;
      this.socket.onerror = null;
      this.socket.onopen = null;
      this.socket.onmessage = null;
      this.socket.close();
      this.socket = null;
    }
  }

  public getState(): ConnectionState {
    return this.state;
  }

  private handleReconnect() {
    const delay = RECONNECT_DELAYS[this.reconnectAttempts] || 30000;
    this.reconnectAttempts++;
    this.setState(ConnectionState.RECONNECTING);

    this.reconnectTimeoutId = setTimeout(() => {
      this.connect();
    }, delay);
  }

  private setState(newState: ConnectionState) {
    if (this.state !== newState) {
      this.state = newState;
      this.emit("state_change", newState);
    }
  }
}
