import { Outlet, useLocation } from "react-router-dom";
import { Suspense, useEffect } from "react";
import Footer from "./Footer";
import Sidebar from "./Sidebar";
import Topbar from "./Topbar";
import Loading from "../components/common/Loading";
import { usePrimaryVehicle } from "../hooks/usePrimaryVehicle";
import { useTelemetrySocket } from "../hooks/useTelemetrySocket";

export default function GlobalLayout() {
  const { vehicleId } = usePrimaryVehicle();
  const { pathname } = useLocation();
  useTelemetrySocket(vehicleId);
  useEffect(() => {
    const page = pathname.slice(1) || "Dashboard";
    document.title = `${page === "bon" ? "BON" : page.charAt(0).toUpperCase() + page.slice(1)} · AutoMind AI`;
    window.scrollTo(0, 0);
  }, [pathname]);
  return (
    <div className="app-shell">
      <a className="skip-link" href="#main-content">
        Skip to content
      </a>
      <Sidebar />
      <div className="app-main">
        <Topbar />
        <main className="content" id="main-content" tabIndex={-1}>
          <Suspense fallback={<Loading />}>
            <Outlet />
          </Suspense>
        </main>
        <Footer />
      </div>
    </div>
  );
}
