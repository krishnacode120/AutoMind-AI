import { Bot } from "lucide-react";

import Card from "../common/Card";

function BonStatusCard() {
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
          <span className="dashboard-card__dot dashboard-card__dot--danger" style={{ background: 'var(--color-muted)', boxShadow: 'none' }} />
          <span className="dashboard-card__label">BON is offline</span>
        </div>
        <p className="dashboard-card__value dashboard-card__value--sm">
          No AI integration yet.
        </p>
      </div>
    </Card>
  );
}

export default BonStatusCard;
