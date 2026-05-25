import { useEffect, useState }
from "react";

import {
  getDashboard
} from "../api/dashboardApi";

import KPICards
from "../components/KPISection";

import HealthBanner
from "../components/HealthBanner";

function Dashboard() {

  const [dashboard, setDashboard] =
    useState(null);

  useEffect(() => {

    const fetchDashboard =
      async () => {

      try {

        const data =
          await getDashboard(43);

        setDashboard(data);

      } catch (error) {

        console.error(error);
      }
    };

    fetchDashboard();

  }, []);

  if (!dashboard) {
    return <h1>Loading...</h1>;
  }

  return (
    <div
      style={{
        padding: "40px",
        background: "#f5f7fb",
        minHeight: "100vh",
      }}
    >
      <h1>
        🤖 AI Insights Dashboard
      </h1>

      <p>
        Business Health:
        <strong>
          {" "}
          {dashboard.business_health}
        </strong>
      </p>

      <KPICards
        kpis={dashboard.kpis}
      />

      <HealthBanner
        health={
          dashboard.business_health
        }
        summary={
          dashboard.summary
        }
      />

    </div>
  );
}

export default Dashboard;