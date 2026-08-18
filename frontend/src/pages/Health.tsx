import PageHeader from "../components/common/PageHeader";
import Card from "../components/common/Card";
import Loading from "../components/common/Loading";
import { useHealth } from "../hooks/useHealth";
import { usePrimaryVehicle } from "../hooks/usePrimaryVehicle";

function Health() {
  const { vehicle, vehicleId, isLoading: vehiclesLoading } = usePrimaryVehicle();
  const { data, isLoading, isError } = useHealth(vehicleId ?? 0);

  return (
    <div className="resource-page">
      <PageHeader title="Health" subtitle="Current deterministic vehicle health assessment" />
      {(vehiclesLoading || isLoading) && <Loading />}
      {!vehiclesLoading && !vehicle && <Card className="resource-card"><p className="resource-empty">Add a vehicle to calculate health.</p></Card>}
      {isError && <Card className="resource-card"><p className="resource-empty">Health data is unavailable until telemetry is recorded.</p></Card>}
      {data && (
        <Card className="resource-card">
          <div className="health-summary"><strong>{data.health_score}%</strong><span>{data.health_status}</span></div>
          <div className="health-card__bar-track"><div className="health-card__bar-fill" style={{ width: `${data.health_score}%` }} /></div>
          <section className="report-section"><h2>Recommendations</h2><ReportList items={data.recommendations} empty="No maintenance recommendations." /></section>
          <section className="report-section"><h2>Penalties</h2><ReportList items={Object.entries(data.penalties).filter(([, value]) => value > 0).map(([name, value]) => `${name.replace("_", " ")}: -${value}`)} empty="No active health penalties." /></section>
        </Card>
      )}
    </div>
  );
}

function ReportList({ items, empty }: { items: string[]; empty: string }) {
  return items.length ? <ul className="report-list">{items.map((item) => <li key={item}>{item}</li>)}</ul> : <p className="resource-empty">{empty}</p>;
}

export default Health;
