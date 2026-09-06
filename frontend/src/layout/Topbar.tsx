import { Moon, Sun, Radio } from "lucide-react";
import { useLocation } from "react-router-dom";
import { useTheme } from "../contexts/ThemeContext";
import { useConnection } from "../contexts/ConnectionContext";
import { ConnectionState } from "../services/websocket/types";
import { usePrimaryVehicle } from "../hooks/usePrimaryVehicle";

export default function Topbar() {
  const { connectionState } = useConnection();
  const { data: vehicles, vehicleId, selectVehicle } = usePrimaryVehicle();
  const { theme, setTheme } = useTheme();
  const page = useLocation().pathname.split("/")[1] || "dashboard";
  const connected = connectionState === ConnectionState.CONNECTED;
  const pending = [
    ConnectionState.CONNECTING,
    ConnectionState.RECONNECTING,
  ].includes(connectionState);
  const status = !vehicleId
    ? "No vehicle selected"
    : connected
      ? "Connected"
      : pending
        ? "Connecting"
        : "Offline";
  return (
    <header className="topbar">
      <div className="breadcrumb">
        Workspace <span>/</span>{" "}
        <strong>{page === "bon" ? "BON assistant" : page}</strong>
      </div>
      <div className="topbar-actions">
        <span
          className={"connection-pill " + (connected ? "is-connected" : "")}
          title="Telemetry stream connection"
        >
          <Radio size={14} />
          {status}
        </span>
        <label className="vehicle-picker">
          <span className="sr-only">Vehicle</span>
          <select
            aria-label="Selected vehicle"
            value={vehicleId ?? ""}
            onChange={(event) => selectVehicle(Number(event.target.value))}
          >
            {!vehicles?.length && <option value="">No vehicles</option>}
            {vehicles?.map((vehicle) => (
              <option key={vehicle.id} value={vehicle.id}>
                {vehicle.name}
              </option>
            ))}
          </select>
        </label>
        <button
          className="icon-button theme-button"
          aria-label={
            theme === "light" ? "Switch to dark theme" : "Switch to light theme"
          }
          onClick={() => setTheme(theme === "light" ? "dark" : "light")}
        >
          {theme === "light" ? <Moon size={18} /> : <Sun size={18} />}
        </button>
      </div>
    </header>
  );
}
