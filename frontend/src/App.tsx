import { Navigate, Route, Routes } from "react-router-dom";
import { lazy, Suspense } from "react";
import Loading from "./components/common/Loading";

import GlobalLayout from "./layout/GlobalLayout";
const Alerts = lazy(() => import("./pages/Alerts"));
const BON = lazy(() => import("./pages/BON"));
const Dashboard = lazy(() => import("./pages/Dashboard"));
const Health = lazy(() => import("./pages/Health"));
const Maintenance = lazy(() => import("./pages/Maintenance"));
const Predictions = lazy(() => import("./pages/Predictions"));
const Settings = lazy(() => import("./pages/Settings"));
const Telemetry = lazy(() => import("./pages/Telemetry"));
const Vehicles = lazy(() => import("./pages/Vehicles"));

function App() {
  return (
    <Suspense fallback={<Loading />}>
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
    </Suspense>
  );
}

export default App;
