import { useEffect, useState } from "react";
import { useQueryClient } from "@tanstack/react-query";
import { TelemetryWebSocketClient } from "../services/websocket/client";
import { ConnectionState } from "../services/websocket/types";
import type {
  Telemetry,
  TelemetryHistory,
  LatestTelemetry,
} from "../types/telemetry";
import { useConnection } from "../contexts/ConnectionContext";
import { parseTimestamp } from "../utils/datetime";

const compareNewest = (a: Telemetry, b: Telemetry) =>
  parseTimestamp(b.timestamp).getTime() -
    parseTimestamp(a.timestamp).getTime() || b.id - a.id;

export function useTelemetrySocket(vehicleId: number | null) {
  const queryClient = useQueryClient();
  const { connectionState, setConnectionState } = useConnection();
  const [lastMessage, setLastMessage] = useState<Telemetry | null>(null);
  useEffect(() => {
    setLastMessage(null);
    if (!vehicleId) {
      setConnectionState(ConnectionState.DISCONNECTED);
      return;
    }
    const client = new TelemetryWebSocketClient(vehicleId);
    let refreshTimer: ReturnType<typeof setTimeout> | undefined;
    const handleStateChange = (state: ConnectionState) =>
      setConnectionState(state);
    const handleMessage = (msg: { type: string; data: Telemetry }) => {
      if (msg.type !== "telemetry_update" || msg.data?.vehicle_id !== vehicleId)
        return;
      setLastMessage((current) =>
        current && compareNewest(current, msg.data) <= 0 ? current : msg.data,
      );
      queryClient.setQueryData<LatestTelemetry>(
        ["telemetry", "latest", vehicleId],
        (current) =>
          current?.telemetry && compareNewest(current.telemetry, msg.data) <= 0
            ? current
            : { vehicle_id: vehicleId, telemetry: msg.data },
      );
      queryClient.setQueryData<TelemetryHistory>(
        ["telemetry", "history", vehicleId],
        (current) =>
          current
            ? {
                ...current,
                records: [
                  msg.data,
                  ...current.records.filter(
                    (record) => record.id !== msg.data.id,
                  ),
                ]
                  .sort(compareNewest)
                  .slice(0, 100),
              }
            : current,
      );
      // A simulated drive emits up to 300 events. Recompute reports once per burst.
      if (!refreshTimer)
        refreshTimer = setTimeout(() => {
          refreshTimer = undefined;
          for (const key of [
            "insights",
            "health",
            "alerts",
            "maintenance",
            "prediction",
          ]) {
            void queryClient.invalidateQueries({ queryKey: [key, vehicleId] });
          }
          void queryClient.invalidateQueries({
            queryKey: ["telemetry", "history", vehicleId],
          });
          void queryClient.invalidateQueries({ queryKey: ["vehicles"] });
        }, 250);
    };
    client.on("state_change", handleStateChange);
    client.on("message", handleMessage);
    client.connect();
    return () => {
      if (refreshTimer) clearTimeout(refreshTimer);
      client.disconnect();
      client.off("state_change", handleStateChange);
      client.off("message", handleMessage);
      setConnectionState(ConnectionState.DISCONNECTED);
    };
  }, [vehicleId, queryClient, setConnectionState]);
  return { connectionState, lastMessage };
}
