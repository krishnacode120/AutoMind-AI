import PageHeader from "../components/common/PageHeader";
import Card from "../components/common/Card";
import { useConnection } from "../contexts/ConnectionContext";

function Settings() {
  const { connectionState } = useConnection();

  return (
    <div className="resource-page">
      <PageHeader title="Settings" subtitle="Application and connection status" />
      <Card className="resource-card">
        <div className="detail-grid">
          <Metric label="Theme" value="Dark" />
          <Metric label="API endpoint" value="127.0.0.1:8000" />
          <Metric label="Telemetry connection" value={connectionState} />
          <Metric label="Assistant" value="BON" />
        </div>
      </Card>
    </div>
  );
}

function Metric({ label, value }: { label: string; value: string }) {
  return <div className="metric"><span>{label}</span><strong>{value}</strong></div>;
}

export default Settings;
