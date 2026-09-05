import { useConnection } from "../contexts/ConnectionContext";
import { ConnectionState } from "../services/websocket/types";
import { usePrimaryVehicle } from "../hooks/usePrimaryVehicle";

function Topbar() {
  const { connectionState } = useConnection();
  const { data: vehicles, vehicleId, selectVehicle } = usePrimaryVehicle();

  const getStatusProps = () => {
    switch (connectionState) {
      case ConnectionState.CONNECTED:
        return { color: "var(--color-success)", text: "Connected" };
      case ConnectionState.CONNECTING:
        return { color: "var(--color-warning)", text: "Connecting" };
      case ConnectionState.RECONNECTING:
        return { color: "var(--color-warning)", text: "Reconnecting" };
      case ConnectionState.ERROR:
        return { color: "var(--color-danger)", text: "Error" };
      case ConnectionState.DISCONNECTED:
      default:
        return { color: "var(--color-danger)", text: "Disconnected" };
    }
  };

  const status = getStatusProps();

  return (
    <header className="topbar">
      <div style={{ display: "flex", alignItems: "center", gap: "16px" }}>
        <div>
          <p className="eyebrow">Vehicle Assistant</p>
          <strong>AutoMind AI</strong>
        </div>
        <div
          style={{
            display: "flex",
            alignItems: "center",
            gap: "8px",
            fontSize: "12px",
            background: "var(--color-panel-soft)",
            padding: "4px 8px",
            borderRadius: "12px",
            border: "1px solid var(--color-border)",
          }}
        >
          <span
            style={{
              width: "8px",
              height: "8px",
              borderRadius: "50%",
              backgroundColor: status.color,
              boxShadow: `0 0 4px ${status.color}`,
            }}
          />
          <span>{status.text}</span>
        </div>
      </div>
      <label className="vehicle-picker">
        Vehicle
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
    </header>
  );
}

export default Topbar;
