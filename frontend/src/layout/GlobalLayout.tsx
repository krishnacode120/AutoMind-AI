import { Outlet } from "react-router-dom";

import Footer from "./Footer";
import Sidebar from "./Sidebar";
import Topbar from "./Topbar";

function GlobalLayout() {
  return (
    <div className="app-shell">
      <Sidebar />
      <div className="app-main">
        <Topbar />
        <main className="content">
          <Outlet />
        </main>
        <Footer />
      </div>
    </div>
  );
}

export default GlobalLayout;
