import {
  Activity,
  AlertTriangle,
  BarChart3,
  Bot,
  Gauge,
  HeartPulse,
  Home,
  Settings,
  Wrench,
} from "lucide-react";
import { NavLink } from "react-router-dom";

const navigationItems = [
  { label: "Dashboard", path: "/dashboard", icon: Home },
  { label: "Vehicles", path: "/vehicles", icon: Gauge },
  { label: "Telemetry", path: "/telemetry", icon: Activity },
  { label: "Health", path: "/health", icon: HeartPulse },
  { label: "Alerts", path: "/alerts", icon: AlertTriangle },
  { label: "Maintenance", path: "/maintenance", icon: Wrench },
  { label: "Predictions", path: "/predictions", icon: BarChart3 },
  { label: "BON", path: "/bon", icon: Bot },
  { label: "Settings", path: "/settings", icon: Settings },
];

function Sidebar() {
  return (
    <aside className="sidebar">
      <div className="brand">
        <span className="brand-mark">A</span>
        <span>AutoMind AI</span>
      </div>
      <nav className="nav-list" aria-label="Primary navigation">
        {navigationItems.map((item) => {
          const Icon = item.icon;

          return (
            <NavLink key={item.path} to={item.path} className="nav-link">
              <Icon size={18} aria-hidden="true" />
              <span>{item.label}</span>
            </NavLink>
          );
        })}
      </nav>
    </aside>
  );
}

export default Sidebar;
