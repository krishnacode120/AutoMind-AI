import { useMutation, useQueryClient } from "@tanstack/react-query";
import { Play } from "lucide-react";
import api, { apiErrorMessage } from "../../services/api";

export default function SimulateDrive({ vehicleId }: { vehicleId: number }) {
  const cache = useQueryClient();
  const mutation = useMutation({
    mutationFn: () =>
      api.post(`/vehicles/${vehicleId}/simulation`, null, { timeout: 60000 }),
    onSuccess: () => cache.invalidateQueries(),
  });
  return (
    <div>
      <button
        className="action-button"
        disabled={mutation.isPending}
        onClick={() => mutation.mutate()}
      >
        <Play size={16} />
        {mutation.isPending ? "Simulating..." : "Simulate drive"}
      </button>
      {mutation.isError && (
        <p role="alert">{apiErrorMessage(mutation.error)}</p>
      )}
      {mutation.isSuccess && (
        <p role="status">60 simulated readings recorded.</p>
      )}
    </div>
  );
}
