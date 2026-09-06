import type { CSSProperties } from "react";
import {
  ArrowRight,
  ArrowUpRight,
  Bot,
  CarFront,
  CheckCircle2,
  Fuel,
  Gauge,
  HeartPulse,
  Thermometer,
  Wrench,
} from "lucide-react";
import { Link } from "react-router-dom";
import PageHeader from "../components/common/PageHeader";
import Loading from "../components/common/Loading";
import EmptyState from "../components/common/EmptyState";
import SimulateDrive from "../components/common/SimulateDrive";
import TelemetryCharts from "../components/charts/TelemetryCharts";
import { usePrimaryVehicle } from "../hooks/usePrimaryVehicle";
import { useLatestTelemetry } from "../hooks/useTelemetry";
import { useInsights } from "../hooks/useInsights";
import { apiErrorMessage } from "../services/api";
import { formatTimestamp } from "../utils/datetime";

export default function Dashboard() {
  const vehicles = usePrimaryVehicle();
  const id = vehicles.vehicleId ?? 0;
  const latest = useLatestTelemetry(id);
  const insights = useInsights(id);
  const vehicle = vehicles.vehicle;
  const telemetry = latest.data?.telemetry;
  const reports = insights.data;
  const score = reports?.health.health_score;
  const attention = (reports?.alerts.alert_count ?? 0) > 0;

  return (
    <div className="dashboard-page">
      <div className="page-toolbar">
        <PageHeader
          title="Dashboard"
          subtitle="A little more insight. A better journey ahead."
        />
        <Link className="text-link" to="/vehicles">
          Manage vehicles <ArrowUpRight size={16} />
        </Link>
      </div>
      {vehicles.isLoading && <Loading />}
      {vehicles.isError ? (
        <EmptyState
          error={apiErrorMessage(vehicles.error)}
          onRetry={() => vehicles.refetch()}
        />
      ) : !vehicles.isLoading && !vehicle ? (
        <EmptyState />
      ) : null}
      {vehicle && (
        <>
          <div className="overview-layout">
            <section className="vehicle-hero">
              <div className="hero-copy">
                <span className="hero-kicker">
                  <span className="status-dot" />
                  YOUR VEHICLE, AT A GLANCE
                </span>
                <h2>{vehicle.name}</h2>
                <p>
                  {vehicle.manufacturer} {vehicle.model} <span>·</span>{" "}
                  {vehicle.year}
                </p>
                <div className="hero-specs">
                  <div>
                    <span>Odometer</span>
                    <strong>
                      {(telemetry?.odometer ?? vehicle.odometer).toLocaleString(
                        undefined,
                        { maximumFractionDigits: 1 },
                      )}
                      <small> km</small>
                    </strong>
                  </div>
                  <div>
                    <span>Powertrain</span>
                    <strong>{vehicle.fuel_type}</strong>
                  </div>
                  <div>
                    <span>Transmission</span>
                    <strong>{vehicle.transmission}</strong>
                  </div>
                </div>
                <span className="hero-footnote">
                  {telemetry
                    ? `Last reading at ${formatTimestamp(telemetry.timestamp)}`
                    : "Ready for its first drive"}
                </span>
              </div>
              <div className="vehicle-art" aria-hidden="true">
                <div className="vehicle-art-ring" />
                <CarFront strokeWidth={0.8} />
                <span>AUTOMIND / CONNECTED VEHICLE</span>
              </div>
            </section>
            <section className="health-overview card">
              <div className="section-heading">
                <h2>Vehicle health</h2>
                <HeartPulse size={18} />
              </div>
              <div
                className={
                  "score-ring " + (attention ? "score-ring--warning" : "")
                }
                style={{ "--score": `${score ?? 0}%` } as CSSProperties}
              >
                <div>
                  <strong>{score ?? "—"}</strong>
                  <span>out of 100</span>
                </div>
              </div>
              <strong>
                {reports?.health.health_status ??
                  (telemetry ? "Calculating health" : "Awaiting telemetry")}
              </strong>
              <p>
                {reports
                  ? attention
                    ? "A few things need your attention."
                    : "No active alerts in the latest reading."
                  : "Run a sample drive to get your first report."}
              </p>
              <Link to="/health" className="text-link">
                View health report <ArrowRight size={15} />
              </Link>
            </section>
          </div>
          <SimulateDrive key={id} vehicleId={id} />
          {latest.isError && (
            <p role="alert" className="inline-error">
              {apiErrorMessage(latest.error)}{" "}
              <button className="text-button" onClick={() => latest.refetch()}>
                Retry telemetry
              </button>
            </p>
          )}
          {insights.isError && (
            <p role="alert" className="inline-error">
              Insights are unavailable.{" "}
              <button
                className="text-button"
                onClick={() => insights.refetch()}
              >
                Retry insights
              </button>
            </p>
          )}
          <div className="stat-grid">
            <Stat
              icon={Gauge}
              label="Current speed"
              value={telemetry?.speed.toFixed(0)}
              unit="km/h"
              hint={
                telemetry?.vehicle_state.replaceAll("_", " ").toLowerCase() ??
                "Awaiting a reading"
              }
            />
            <Stat
              icon={Fuel}
              label="Fuel level"
              value={telemetry?.fuel_level.toFixed(1)}
              unit="%"
              hint={
                telemetry
                  ? telemetry.fuel_level < 20
                    ? "Refuel soon"
                    : "Fuel in the tank"
                  : "Awaiting a reading"
              }
              warning={!!telemetry && telemetry.fuel_level < 20}
            />
            <Stat
              icon={Thermometer}
              label="Engine temperature"
              value={telemetry?.engine_temperature.toFixed(1)}
              unit="°C"
              hint={
                telemetry
                  ? telemetry.engine_temperature > 100
                    ? "Above normal range"
                    : "Latest engine reading"
                  : "Awaiting a reading"
              }
              warning={!!telemetry && telemetry.engine_temperature > 100}
            />
            <Stat
              icon={Wrench}
              label="Maintenance tasks"
              value={reports?.maintenance.task_count.toString()}
              unit="tasks"
              hint={
                reports
                  ? reports.maintenance.task_count
                    ? "Review recommended actions"
                    : "Nothing due right now"
                  : "Awaiting assessment"
              }
            />
          </div>
          <div className="dashboard-detail-layout">
            <TelemetryCharts vehicleId={id} />
            <section className="attention-card card">
              <div className="section-heading">
                <h2>Needs attention</h2>
                <Link to="/alerts" className="text-link">
                  View all <ArrowUpRight size={14} />
                </Link>
              </div>
              {reports ? (
                reports.alerts.alerts.length ? (
                  <div className="attention-list">
                    {reports.alerts.alerts.slice(0, 3).map((alert) => (
                      <Link
                        to="/alerts"
                        key={alert.type}
                        className="attention-item"
                      >
                        <span
                          className={`priority priority--${alert.severity.toLowerCase()}`}
                        >
                          {alert.severity.toLowerCase()}
                        </span>
                        <strong>{alert.title}</strong>
                        <p>{alert.recommendation}</p>
                      </Link>
                    ))}
                  </div>
                ) : (
                  <div className="all-clear">
                    <CheckCircle2 size={34} />
                    <h3>You’re all caught up.</h3>
                    <p>
                      No active alerts. New insights appear here when your
                      readings change.
                    </p>
                  </div>
                )
              ) : (
                <div className="all-clear">
                  <HeartPulse size={32} />
                  <h3>Your insights start with data.</h3>
                  <p>Simulate a drive to check the systems that matter.</p>
                </div>
              )}
            </section>
          </div>
          <section className="bon-invitation">
            <div className="bon-invitation-icon">
              <Bot size={28} />
            </div>
            <div>
              <p className="eyebrow">MEET BON, YOUR VEHICLE ASSISTANT</p>
              <h2>Data is useful. Understanding it is better.</h2>
              <p>
                Ask about your vehicle’s health, alerts, or what to do next.
              </p>
            </div>
            <Link to="/bon" className="action-button primary">
              Ask BON <ArrowUpRight size={16} />
            </Link>
          </section>
        </>
      )}
    </div>
  );
}

function Stat({
  icon: Icon,
  label,
  value,
  unit,
  hint,
  warning = false,
}: {
  icon: typeof Gauge;
  label: string;
  value?: string;
  unit: string;
  hint: string;
  warning?: boolean;
}) {
  return (
    <section
      className={"stat-card card " + (warning ? "stat-card--warning" : "")}
    >
      <div className="stat-label">
        <span>{label}</span>
        <Icon size={18} />
      </div>
      <p className="stat-value">
        {value ?? "—"} <span>{unit}</span>
      </p>
      <p className="stat-hint">
        <span className="status-dot" />
        {hint}
      </p>
    </section>
  );
}
