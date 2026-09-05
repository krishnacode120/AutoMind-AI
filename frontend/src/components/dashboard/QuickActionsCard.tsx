import { FileSearch, Fuel, Wrench, Zap } from "lucide-react";

import Card from "../common/Card";
import { Link } from "react-router-dom";

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
          <Link to="/health" className="quick-actions__btn">
            <Wrench size={16} className="quick-actions__btn-icon" />
            <span>View health</span>
          </Link>
          <Link to="/telemetry" className="quick-actions__btn">
            <Fuel size={16} className="quick-actions__btn-icon" />
            <span>View telemetry</span>
          </Link>
          <Link to="/maintenance" className="quick-actions__btn">
            <FileSearch size={16} className="quick-actions__btn-icon" />
            <span>View maintenance</span>
          </Link>
        </div>
      </div>
    </Card>
  );
}

export default QuickActionsCard;
