import PageHeader from "../components/common/PageHeader";
import Card from "../components/common/Card";
import { useConnection } from "../contexts/ConnectionContext";
import { API_BASE_URL } from "../services/api";

function Settings() {
  const { connectionState } = useConnection();

  return (
    <div className="resource-page">
      <PageHeader
        title="Settings"
        subtitle="Application and connection status"
      />
      <Card className="resource-card">
        <div className="detail-grid">
          <Metric label="Theme" value="Dark" />
          <Metric label="API endpoint" value={API_BASE_URL} />
          <Metric label="Telemetry connection" value={connectionState} />
          <Metric label="Assistant" value="BON" />
        </div>
      </Card>
    </div>
  );
}

function Metric({ label, value }: { label: string; value: string }) {
  return (
    <div className="metric">
      <span>{label}</span>
      <strong>{value}</strong>
    </div>
  );
}

export default Settings;
