import { Sun, Moon, Radio } from "lucide-react";
import PageHeader from "../components/common/PageHeader";
import { useConnection } from "../contexts/ConnectionContext";
import { useTheme } from "../contexts/ThemeContext";
import { useQuery } from "@tanstack/react-query";
import api from "../services/api";
export default function Settings() {
  const { connectionState } = useConnection();
  const { theme, setTheme } = useTheme();
  const health = useQuery({
    queryKey: ["system-health"],
    queryFn: async () => (await api.get("/health")).data,
  });
  return (
    <div className="resource-page">
      <PageHeader
        title="Settings"
        subtitle="Make this workspace feel like yours."
      />
      <section className="card resource-card settings-section">
        <div>
          <h2>Appearance</h2>
          <p>Choose your preferred look. Saved in this browser.</p>
        </div>
        <div className="theme-options">
          <button
            className="theme-option"
            aria-pressed={theme === "light"}
            onClick={() => setTheme("light")}
          >
            <Sun size={22} />
            <strong>Light</strong>
            <span>A fresh, open workspace</span>
          </button>
          <button
            className="theme-option"
            aria-pressed={theme === "dark"}
            onClick={() => setTheme("dark")}
          >
            <Moon size={22} />
            <strong>Dark</strong>
            <span>Comfort for late-night drives</span>
          </button>
        </div>
      </section>
      <section className="card resource-card">
        <h2>Connection status</h2>
        <div className="detail-grid">
          <div className="metric">
            <span>Vehicle data service</span>
            <strong>
              {health.isLoading
                ? "Checking…"
                : health.isError
                  ? "Unavailable"
                  : "Available"}
            </strong>
          </div>
          <div className="metric">
            <span>Telemetry stream</span>
            <strong className="connection-setting">
              <Radio size={16} />
              {connectionState.toLowerCase()}
            </strong>
          </div>
          <div className="metric">
            <span>Assistant</span>
            <strong>BON · contextual guidance</strong>
          </div>
        </div>
        {health.isError && (
          <button className="action-button" onClick={() => health.refetch()}>
            Check connection again
          </button>
        )}
      </section>
      <section className="card resource-card">
        <h2>About your workspace</h2>
        <p className="report-summary">
          AutoMind AI 2.0 brings vehicle records, sample drives, diagnostics,
          and conversational guidance together. Sample drives generate synthetic
          data. BON uses vehicle context and rules without requiring an external
          AI account.
        </p>
      </section>
    </div>
  );
}
