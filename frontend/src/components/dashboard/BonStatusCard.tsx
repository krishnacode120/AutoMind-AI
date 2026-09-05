import { Bot } from "lucide-react";

import Card from "../common/Card";
import { useQuery } from "@tanstack/react-query";
import api from "../../services/api";

function BonStatusCard() {
  const { data, isPending, isError } = useQuery({
    queryKey: ["bon-status"],
    queryFn: async () =>
      (await api.get<{ status: string }>("/bon/health")).data,
  });
  return (
    <Card className="dashboard-card" animated>
      <div className="dashboard-card__header">
        <h2 className="dashboard-card__title">BON Status</h2>
        <div className="dashboard-card__icon dashboard-card__icon--danger">
          <Bot size={20} />
        </div>
      </div>
      <div className="dashboard-card__body">
        <div className="dashboard-card__status">
          <span
            className="dashboard-card__dot dashboard-card__dot--danger"
            style={{ background: "var(--color-muted)", boxShadow: "none" }}
          />
          <span className="dashboard-card__label">
            {isPending
              ? "Checking BON..."
              : isError
                ? "BON is unavailable"
                : `BON is ${data?.status}`}
          </span>
        </div>
        <p className="dashboard-card__value dashboard-card__value--sm">
          Vehicle assistant
        </p>
      </div>
    </Card>
  );
}

export default BonStatusCard;
