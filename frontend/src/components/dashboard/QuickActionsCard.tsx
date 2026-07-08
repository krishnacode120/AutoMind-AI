import { FileSearch, Fuel, Wrench, Zap } from "lucide-react";

import Card from "../common/Card";

function QuickActionsCard() {
  return (
    <Card className="dashboard-card" animated>
      <div className="dashboard-card__header">
        <h2 className="dashboard-card__title">Quick Actions</h2>
        <div className="dashboard-card__icon dashboard-card__icon--primary">
          <Zap size={20} />
        </div>
      </div>
      <div className="dashboard-card__body">
        <div className="quick-actions__list">
          <button type="button" className="quick-actions__btn" disabled style={{ opacity: 0.5, cursor: "not-allowed" }}>
            <Wrench size={16} className="quick-actions__btn-icon" />
            <span>Run Diagnostics</span>
          </button>
          <button type="button" className="quick-actions__btn" disabled style={{ opacity: 0.5, cursor: "not-allowed" }}>
            <Fuel size={16} className="quick-actions__btn-icon" />
            <span>Check Fuel System</span>
          </button>
          <button type="button" className="quick-actions__btn" disabled style={{ opacity: 0.5, cursor: "not-allowed" }}>
            <FileSearch size={16} className="quick-actions__btn-icon" />
            <span>View Maintenance Log</span>
          </button>
        </div>
      </div>
    </Card>
  );
}

export default QuickActionsCard;
