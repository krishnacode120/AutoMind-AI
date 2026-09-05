import { useEffect, useState } from "react";
import { useQueryClient } from "@tanstack/react-query";
import { TelemetryWebSocketClient } from "../services/websocket/client";
import { ConnectionState } from "../services/websocket/types";
import type { Telemetry, TelemetryHistory } from "../types/telemetry";
import { useConnection } from "../contexts/ConnectionContext";

export function useTelemetrySocket(vehicleId: number | null) {
  const queryClient = useQueryClient();
  const { connectionState, setConnectionState } = useConnection();
  const [lastMessage, setLastMessage] = useState<Telemetry | null>(null);

  useEffect(() => {
    if (!vehicleId) return;

    const client = new TelemetryWebSocketClient(vehicleId);

    const handleStateChange = (state: ConnectionState) => {
      setConnectionState(state);
    };

    const handleMessage = (msg: { type: string; data: Telemetry }) => {
      if (msg.type === "telemetry_update") {
        setLastMessage(msg.data);

        // Update latest telemetry cache
        queryClient.setQueryData(["telemetry", "latest", vehicleId], {
          vehicle_id: vehicleId,
          telemetry: msg.data,
        });

        queryClient.setQueryData<TelemetryHistory>(
          ["telemetry", "history", vehicleId],
          (oldData) => {
            if (!oldData) return { vehicle_id: vehicleId, records: [msg.data] };

            const newRecords = [
              msg.data,
              ...oldData.records.filter((record) => record.id !== msg.data.id),
            ]
              .sort(
                (a, b) =>
                  Date.parse(b.timestamp) - Date.parse(a.timestamp) ||
                  b.id - a.id,
              )
              .slice(0, 100);
            return {
              ...oldData,
              records: newRecords,
            };
          },
        );
        for (const key of ["health", "alerts", "maintenance", "prediction"]) {
          void queryClient.invalidateQueries({ queryKey: [key, vehicleId] });
        }
      }
    };

    client.on("state_change", handleStateChange);
    client.on("message", handleMessage);

    client.connect();

    return () => {
      client.disconnect();
      client.off("state_change", handleStateChange);
      client.off("message", handleMessage);
      setConnectionState(ConnectionState.DISCONNECTED);
    };
  }, [vehicleId, queryClient, setConnectionState]);

  return { connectionState, lastMessage };
}
