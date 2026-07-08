import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter } from "react-router-dom";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";

import App from "./App";
import { ThemeProvider } from "./contexts/ThemeContext";
import { ConnectionProvider } from "./contexts/ConnectionContext";
import "./styles/global.css";

const queryClient = new QueryClient();

ReactDOM.createRoot(document.getElementById("root") as HTMLElement).render(
  <React.StrictMode>
    <QueryClientProvider client={queryClient}>
      <ThemeProvider>
        <ConnectionProvider>
          <BrowserRouter>
            <App />
          </BrowserRouter>
        </ConnectionProvider>
      </ThemeProvider>
    </QueryClientProvider>
  </React.StrictMode>,
);


