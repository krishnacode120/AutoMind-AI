import { useState } from "react";
import { Activity } from "lucide-react";
import {
  ResponsiveContainer,
  LineChart,
  CartesianGrid,
  XAxis,
  YAxis,
  Tooltip,
  Line,
} from "recharts";
import { useTelemetryHistory } from "../../hooks/useTelemetry";
import { formatTimestamp, parseTimestamp } from "../../utils/datetime";
import Loading from "../common/Loading";
import Card from "../common/Card";

const metrics = {
  speed: { label: "Speed", unit: "km/h", color: "var(--color-accent)" },
  rpm: { label: "RPM", unit: "rpm", color: "var(--color-primary)" },
  engine_temperature: {
    label: "Temperature",
    unit: "°C",
    color: "var(--color-warning)",
  },
  fuel_level: { label: "Fuel", unit: "%", color: "var(--color-accent)" },
};
export default function TelemetryCharts({ vehicleId }: { vehicleId: number }) {
  const query = useTelemetryHistory(vehicleId);
  const [metric, setMetric] = useState<keyof typeof metrics>("speed");
  const selected = metrics[metric];
  const records = [...(query.data?.records ?? [])].sort(
    (a, b) =>
      parseTimestamp(a.timestamp).getTime() -
        parseTimestamp(b.timestamp).getTime() || a.id - b.id,
  );
  return (
    <Card className="telemetry-chart">
      <div className="section-heading">
        <div>
          <h2>Telemetry overview</h2>
          <p>
            Latest {records.length} readings · {selected.unit}
          </p>
        </div>
        <Activity size={19} />
      </div>
      <div className="chart-tabs" aria-label="Chart metric">
        {Object.entries(metrics).map(([key, item]) => (
          <button
            key={key}
            aria-pressed={metric === key}
            onClick={() => setMetric(key as keyof typeof metrics)}
          >
            {item.label}
          </button>
        ))}
      </div>
      {query.isLoading ? (
        <Loading />
      ) : query.isError ? (
        <div className="chart-empty">
          <p>Telemetry history could not be loaded.</p>
          <button className="action-button" onClick={() => query.refetch()}>
            Retry history
          </button>
        </div>
      ) : !records.length ? (
        <div className="chart-empty">
          <Activity size={30} />
          <strong>Your next drive, in detail.</strong>
          <p>Recorded readings will appear here.</p>
        </div>
      ) : (
        <div
          className="chart-canvas"
          role="img"
          aria-label={`${selected.label} over the latest ${records.length} readings. Latest value: ${records.at(-1)?.[metric]} ${selected.unit}.`}
        >
          <ResponsiveContainer width="100%" height="100%">
            <LineChart
              data={records}
              margin={{ top: 18, right: 14, left: -14, bottom: 10 }}
            >
              <CartesianGrid
                vertical={false}
                strokeDasharray="3 5"
                stroke="var(--color-border)"
              />
              <XAxis
                dataKey="timestamp"
                tickFormatter={formatTimestamp}
                minTickGap={55}
                tickLine={false}
                axisLine={false}
                tick={{ fill: "var(--color-muted)", fontSize: 11 }}
                dy={8}
              />
              <YAxis
                tickLine={false}
                axisLine={false}
                tick={{ fill: "var(--color-muted)", fontSize: 11 }}
                domain={metric === "fuel_level" ? [0, 100] : [0, "auto"]}
              />
              <Tooltip
                labelFormatter={(label) => formatTimestamp(String(label))}
                contentStyle={{
                  background: "var(--color-panel)",
                  color: "var(--color-text)",
                  border: "1px solid var(--color-border)",
                  borderRadius: 12,
                }}
              />
              <Line
                type="monotone"
                dataKey={metric}
                name={selected.label}
                unit={` ${selected.unit}`}
                stroke={selected.color}
                strokeWidth={2.5}
                dot={records.length === 1}
                isAnimationActive={false}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      )}
      <div className="chart-footer">
        <span className="status-dot" />
        Recorded telemetry <span>Updates automatically</span>
      </div>
    </Card>
  );
}
