import { useState } from "react";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { FlaskConical, Play } from "lucide-react";
import api, { apiErrorMessage } from "../../services/api";
import type { ApiResponse } from "../../types/common";

export default function SimulateDrive({ vehicleId }: { vehicleId: number }) {
  const cache = useQueryClient();
  const [scenario, setScenario] = useState("normal");
  const [samples, setSamples] = useState(60);
  const mutation = useMutation({
    mutationFn: async () =>
      (
        await api.post<ApiResponse<{ samples: number }>>(
          `/vehicles/${vehicleId}/simulation`,
          null,
          { params: { scenario, samples }, timeout: 60000 },
        )
      ).data.data,
    onSuccess: async () => {
      await cache.invalidateQueries();
    },
  });
  return (
    <section className="simulation-bar">
      <div className="simulation-copy">
        <FlaskConical size={19} />
        <div>
          <strong>Drive simulator</strong>
          <span>
            Generate a sample drive to explore your vehicle’s insights.
          </span>
        </div>
      </div>
      <div className="simulation-controls">
        <select
          aria-label="Simulation scenario"
          value={scenario}
          disabled={mutation.isPending}
          onChange={(e) => {
            setScenario(e.target.value);
            mutation.reset();
          }}
        >
          <option value="normal">Normal drive</option>
          <option value="overheating">Overheating</option>
          <option value="low_fuel">Low fuel</option>
          <option value="worn_brakes">Worn brakes</option>
        </select>
        <select
          aria-label="Simulation readings"
          value={samples}
          disabled={mutation.isPending}
          onChange={(e) => {
            setSamples(Number(e.target.value));
            mutation.reset();
          }}
        >
          <option value={60}>60 readings</option>
          <option value={120}>120 readings</option>
          <option value={300}>300 readings</option>
        </select>
        <button
          className="action-button primary"
          disabled={mutation.isPending}
          onClick={() => mutation.mutate()}
        >
          <Play size={15} />
          {mutation.isPending ? "Simulating…" : "Simulate drive"}
        </button>
      </div>
      {mutation.isError && (
        <p className="simulation-feedback danger" role="alert">
          {apiErrorMessage(mutation.error)}
        </p>
      )}
      {mutation.isSuccess && (
        <p className="simulation-feedback" role="status">
          {mutation.data.samples} simulated readings recorded.
        </p>
      )}
    </section>
  );
}
