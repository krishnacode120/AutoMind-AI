import {
  ResponsiveContainer,
  LineChart,
  CartesianGrid,
  XAxis,
  YAxis,
  Tooltip,
  Legend,
  Line,
} from "recharts";
import type { Telemetry } from "../../types/telemetry";
import Card from "../common/Card";

type Props = {
  data: Telemetry[];
};

function TemperatureChart({ data }: Props) {
  const formattedData = data.map((d) => ({
    ...d,
    time: new Date(d.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' }),
  }));

  return (
    <Card className="dashboard-card">
      <div className="dashboard-card__header" style={{ marginBottom: "16px" }}>
        <h2 className="dashboard-card__title">Engine Temperature</h2>
      </div>
      <div style={{ width: "100%", height: 300 }}>
        <ResponsiveContainer>
          <LineChart data={formattedData} margin={{ top: 5, right: 20, bottom: 5, left: 0 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="var(--color-border)" />
            <XAxis dataKey="time" stroke="var(--color-muted)" fontSize={12} tickMargin={10} />
            <YAxis stroke="var(--color-muted)" fontSize={12} unit="°C" />
            <Tooltip 
              contentStyle={{ backgroundColor: "var(--color-panel-soft)", border: "1px solid var(--color-border)", borderRadius: "8px" }}
              itemStyle={{ color: "var(--color-text)" }}
            />
            <Legend />
            <Line type="monotone" dataKey="engine_temperature" name="Temperature (°C)" stroke="var(--color-danger)" strokeWidth={2} dot={false} activeDot={{ r: 6 }} />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </Card>
  );
}

export default TemperatureChart;
