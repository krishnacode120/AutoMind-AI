import React, { createContext, useContext, useState } from "react";
import { ConnectionState } from "../services/websocket/types";

type ConnectionContextType = {
  connectionState: ConnectionState;
  setConnectionState: (state: ConnectionState) => void;
};

const ConnectionContext = createContext<ConnectionContextType | undefined>(undefined);

export function ConnectionProvider({ children }: { children: React.ReactNode }) {
  const [connectionState, setConnectionState] = useState<ConnectionState>(ConnectionState.DISCONNECTED);

  return (
    <ConnectionContext.Provider value={{ connectionState, setConnectionState }}>
      {children}
    </ConnectionContext.Provider>
  );
}

export function useConnection() {
  const context = useContext(ConnectionContext);
  if (!context) {
    throw new Error("useConnection must be used within a ConnectionProvider");
  }
  return context;
}
