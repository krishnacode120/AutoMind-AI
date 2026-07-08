import { ConnectionState, TelemetrySocketMessage } from "./types";
import { EventEmitter } from "./events";

const MAX_RECONNECT_ATTEMPTS = 5;
const RECONNECT_DELAYS = [1000, 2000, 4000, 8000, 30000]; // Defined backoff delays

export class TelemetryWebSocketClient extends EventEmitter {
  private socket: WebSocket | null = null;
  private url: string;
  private state: ConnectionState = ConnectionState.DISCONNECTED;
  private reconnectAttempts = 0;
  private reconnectTimeoutId: ReturnType<typeof setTimeout> | null = null;

  constructor(vehicleId: number) {
    super();
    // Assuming backend runs on the same host or dynamically relative
    // Fallback to local development server if needed
    const protocol = window.location.protocol === "https:" ? "wss:" : "ws:";
    const host = window.location.hostname === "localhost" ? "localhost:8000" : window.location.host;
    this.url = `${protocol}//${host}/api/v1/ws/telemetry/${vehicleId}`;
  }

  public connect() {
    if (this.socket && (this.socket.readyState === WebSocket.OPEN || this.socket.readyState === WebSocket.CONNECTING)) {
      return;
    }

    this.setState(this.reconnectAttempts === 0 ? ConnectionState.CONNECTING : ConnectionState.RECONNECTING);

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
      this.socket.close();
      this.socket = null;
    }
  }

  public getState(): ConnectionState {
    return this.state;
  }

  private handleReconnect() {
    if (this.reconnectAttempts >= MAX_RECONNECT_ATTEMPTS) {
      this.setState(ConnectionState.DISCONNECTED);
      return;
    }

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
