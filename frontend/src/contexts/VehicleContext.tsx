import { createContext, useContext, useState, type ReactNode } from "react";
import { useVehicles } from "../hooks/useVehicle";

const VehicleContext = createContext<ReturnType<
  typeof useVehicleSelection
> | null>(null);

function useVehicleSelection() {
  const query = useVehicles();
  const [selectedId, setSelectedId] = useState<number | null>(() => {
    try {
      return Number(localStorage.getItem("automind-vehicle")) || null;
    } catch {
      return null;
    }
  });
  const vehicle =
    query.data?.find((item) => item.id === selectedId) ??
    query.data?.[0] ??
    null;
  function selectVehicle(id: number) {
    setSelectedId(id);
    try {
      localStorage.setItem("automind-vehicle", String(id));
    } catch {
      /* Storage is optional. */
    }
  }
  return { ...query, vehicle, vehicleId: vehicle?.id ?? null, selectVehicle };
}

export function VehicleProvider({ children }: { children: ReactNode }) {
  const value = useVehicleSelection();
  return (
    <VehicleContext.Provider value={value}>{children}</VehicleContext.Provider>
  );
}

export function useSelectedVehicle() {
  const context = useContext(VehicleContext);
  if (!context) throw new Error("VehicleProvider is required");
  return context;
}
