import {
  Activity,
  AlertTriangle,
  BarChart3,
  Bot,
  CarFront,
  HeartPulse,
  LayoutDashboard,
  Settings,
  Wrench,
  ArrowUpRight,
  Route,
} from "lucide-react";
import { NavLink, Link } from "react-router-dom";

const groups = [
  {
    title: "WORKSPACE",
    items: [
      { label: "Dashboard", path: "/dashboard", icon: LayoutDashboard },
      { label: "Vehicles", path: "/vehicles", icon: CarFront },
      { label: "Telemetry", path: "/telemetry", icon: Activity },
    ],
  },
  {
    title: "INTELLIGENCE",
    items: [
      { label: "Health", path: "/health", icon: HeartPulse },
      { label: "Alerts", path: "/alerts", icon: AlertTriangle },
      { label: "Maintenance", path: "/maintenance", icon: Wrench },
      { label: "Predictions", path: "/predictions", icon: BarChart3 },
      { label: "BON", path: "/bon", icon: Bot },
    ],
  },
];
export default function Sidebar() {
  return (
    <aside className="sidebar">
      <Link to="/dashboard" className="brand" aria-label="AutoMind AI home">
        <span className="brand-mark">
          <Route size={23} />
        </span>
        <span>
          AutoMind<span className="brand-ai"> AI</span>
          <small>VEHICLE INTELLIGENCE</small>
        </span>
      </Link>
      <nav aria-label="Primary navigation" className="navigation">
        {groups.map((group) => (
          <div className="nav-group" key={group.title}>
            <p className="nav-caption">{group.title}</p>
            <div className="nav-list">
              {group.items.map(({ label, path, icon: Icon }) => (
                <NavLink key={path} to={path} className="nav-link">
                  <Icon size={18} />
                  <span>{label}</span>
                  {label === "BON" && (
                    <span className="nav-tag" aria-hidden="true">
                      AI
                    </span>
                  )}
                </NavLink>
              ))}
            </div>
          </div>
        ))}
        <NavLink to="/settings" className="nav-link settings-link">
          <Settings size={18} />
          <span>Settings</span>
        </NavLink>
      </nav>
      <div className="sidebar-note">
        <span className="status-dot" />
        Built for the road ahead
        <p>Turn vehicle data into your next best action.</p>
        <Link to="/bon">
          Meet your assistant <ArrowUpRight size={16} />
        </Link>
      </div>
      <div className="sidebar-version">
        <span>AutoMind workspace</span>
        <span>v2.0</span>
      </div>
    </aside>
  );
}
