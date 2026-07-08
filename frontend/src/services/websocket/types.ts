export enum ConnectionState {
  CONNECTING = "CONNECTING",
  CONNECTED = "CONNECTED",
  RECONNECTING = "RECONNECTING",
  DISCONNECTED = "DISCONNECTED",
  ERROR = "ERROR",
}

export interface TelemetrySocketMessage {
  type: string;
  data: any;
}
