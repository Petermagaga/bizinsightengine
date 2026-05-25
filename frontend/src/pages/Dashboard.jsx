import { useEffect, useState }
from "react";

import AlertsPanel from "../components/AlertPanel";
import RecommendationsPanel from "../components/RecommendationsPanel";
import {
  getDashboard
} from "../api/dashboardApi";


import DecisionsPanel from "../components/DecisionsPanel";
import KPICards
from "../components/KPISection";

import ForecastChart from "../components/ForecastChart";
import TimeSeriesInsights from "../components/TimeSeriesChart";
import HealthBanner
from "../components/HealthBanner";

import ProductionChart from "../components/ProductionChart";
import SummaryCard from "../components/SummaryCard";

function Dashboard() {

  const [dashboard, setDashboard] =
    useState(null);

  const [loading, setLoading] =
    useState(true);

  useEffect(() => {

    const fetchDashboard =
      async () => {

      try {

        const data =
          await getDashboard(43);

        setDashboard(data);

      } catch (error) {

        console.error(error);

      } finally {

        setLoading(false);
      }
    };

    fetchDashboard();

  }, []);

  if (loading) {
    return (
      <div
        style={{
          height: "100vh",
          display: "flex",
          justifyContent:
            "center",
          alignItems:
            "center",
          fontSize: "24px",
          fontWeight: "bold",
        }}
      >
        Loading Dashboard...
      </div>
    );
  }
  console.log(dashboard);
  console.log(dashboard.forecast_chart);



return (

<div
  style={{
    maxWidth: "1400px",
    margin: "0 auto",
    padding: "30px",
  }}
>


  <div
    style={{
      background: "#d5eca0ff",
      minHeight: "100vh",
      padding: "30px",
    }}
  >

<div
  style={{
    marginBottom: "30px",
  }}
>
  <h1
    style={{
      fontSize: "34px",
      fontWeight: "700",
    }}
  >
    AI Insights Dashboard
  </h1>

  <p
    style={{
      marginTop: "8px",
      fontSize: "16px",
      color: "#665e64ff",
    }}
  >
    Real-time business intelligence,
    forecasting, and operational
    insights
  </p>
</div>



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

    <SummaryCard
      summary={
        dashboard.summary
      }
    />

    <div
      style={{
        display: "grid",
        gridTemplateColumns:
          "2fr 1fr",
        gap: "20px",
        marginTop: "20px",
      }}
    >
      <ProductionChart
        timeSeries={
          dashboard.time_series
        }
      />

      <TimeSeriesInsights
        timeSeries={
          dashboard.time_series
        }
      />
    </div>

    <ForecastChart
      forecastData={
        dashboard.forecast_chart
      }
    />

  <div
    style={{
      display: "grid",
      gridTemplateColumns:
        "1fr 1fr",
      gap: "20px",
      marginTop: "20px",
    }}
  >
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

  <div
    style={{
      marginTop: "20px",
    }}
  >
    <DecisionsPanel
      decisions={
        dashboard.decisions
      }
    />
  </div>


  </div>
  </div>
);
}

export default Dashboard;