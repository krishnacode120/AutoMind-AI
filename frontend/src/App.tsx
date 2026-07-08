import { Navigate, Route, Routes } from "react-router-dom";

import GlobalLayout from "./layout/GlobalLayout";
import Alerts from "./pages/Alerts";
import BON from "./pages/BON";
import Dashboard from "./pages/Dashboard";
import Health from "./pages/Health";
import Maintenance from "./pages/Maintenance";
import Predictions from "./pages/Predictions";
import Settings from "./pages/Settings";
import Telemetry from "./pages/Telemetry";
import Vehicles from "./pages/Vehicles";

function App() {
  return (
    <Routes>
      <Route element={<GlobalLayout />}>
        <Route index element={<Navigate to="/dashboard" replace />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/vehicles" element={<Vehicles />} />
        <Route path="/telemetry" element={<Telemetry />} />
        <Route path="/health" element={<Health />} />
        <Route path="/alerts" element={<Alerts />} />
        <Route path="/maintenance" element={<Maintenance />} />
        <Route path="/predictions" element={<Predictions />} />
        <Route path="/bon" element={<BON />} />
        <Route path="/settings" element={<Settings />} />
        <Route path="*" element={<Navigate to="/dashboard" replace />} />
      </Route>
    </Routes>
  );
}

export default App;
