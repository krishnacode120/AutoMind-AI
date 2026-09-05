import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter } from "react-router-dom";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";

import App from "./App";
import { ThemeProvider } from "./contexts/ThemeContext";
import { ConnectionProvider } from "./contexts/ConnectionContext";
import { VehicleProvider } from "./contexts/VehicleContext";
import "./styles/global.css";
import "./styles/workflows.css";

const queryClient = new QueryClient({
  defaultOptions: {
    queries: { retry: 1, staleTime: 3000, refetchInterval: 5000 },
  },
});

ReactDOM.createRoot(document.getElementById("root") as HTMLElement).render(
  <React.StrictMode>
    <QueryClientProvider client={queryClient}>
      <ThemeProvider>
        <ConnectionProvider>
          <VehicleProvider>
            <BrowserRouter>
              <App />
            </BrowserRouter>
          </VehicleProvider>
        </ConnectionProvider>
      </ThemeProvider>
    </QueryClientProvider>
  </React.StrictMode>,
);
