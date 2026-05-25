import { useEffect, useState }
from "react";

import AlertsPanel from "../components/AlertPanel";
import RecommendationsPanel from "../components/RecommendationsPanel";
import {
  getDashboard
} from "../api/dashboardApi";

import KPICards
from "../components/KPISection";

import ForecastChart from "../components/ForecastChart";

import HealthBanner
from "../components/HealthBanner";

import ProductionChart from "../components/ProductionChart";

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

  console.log(dashboard);
  console.log(dashboard.forecast_chart);

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

      <ProductionChart
        timeSeries={
          dashboard.time_series
        }
      />

      <ForecastChart
        forecastData={
          dashboard.forecast_chart
        }
      />
      <AlertsPanel
        alerts={
          dashboard.alerts
        }  

      />
      <RecommendationsPanel
      
      recommendations={
        dashboard.recommendations
      }
      />
    </div>
  );
}

export default Dashboard;