import { useEffect, useState } from "react";
import { useQueryClient } from "@tanstack/react-query";
import { TelemetryWebSocketClient } from "../services/websocket/client";
import { ConnectionState } from "../services/websocket/types";
import { Telemetry } from "../types/telemetry";
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

        // Update telemetry history cache (append and slice to keep last 100)
        queryClient.setQueryData(["telemetry", "history", vehicleId], (oldData: any) => {
          if (!oldData) return { vehicle_id: vehicleId, records: [msg.data] };
          
          const newRecords = [...oldData.records, msg.data];
          if (newRecords.length > 100) {
            newRecords.shift(); // Remove oldest to keep 100
          }
          return {
            ...oldData,
            records: newRecords,
          };
        });
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

