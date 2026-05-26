import { useEffect, useState }
from "react";

import AlertsPanel from "../components/AlertPanel";
import RecommendationsPanel from "../components/RecommendationsPanel";
import {
  getDashboard
} from "../api/dashboardApi";

import { getDatasets } from "../api/datasetApi";
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

  const [datasets, setDatasets] =
    useState([]);

  const [selectedDataset, setSelectedDataset] =
    useState(null);


  useEffect(() => {

    const fetchDashboard =
      async () => {

      try {

        const datasetList =
          await getDatasets();

        setDatasets(datasetList);

        if (
          datasetList.length === 0
        ) {
          return;
        }

        const latestDataset =
          datasetList[0];

        setSelectedDataset(
          latestDataset.id
        );

        const data =
          await getDashboard(
            latestDataset.id
          );

        setDashboard(data);

      } catch (error) {

        console.error(error);

      } finally {

        setLoading(false);
      }
    };

    fetchDashboard();

  }, []);


  const handleDatasetChange =
    async (e) => {

    const datasetId =
      e.target.value;

    setSelectedDataset(
      datasetId
    );

    setLoading(true);

    try {

      const data =
        await getDashboard(
          datasetId
        );

      setDashboard(data);

    } catch (error) {

      console.error(error);

    } finally {

      setLoading(false);
    }
  };

  if (loading || !dashboard) {
    return (
      <div
        style={{
          height: "100vh",
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          fontSize: "24px",
          fontWeight: "bold",
        }}
      >
        Loading Dashboard...
      </div>
    );
  }


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

<div
  style={{
    marginTop: "20px",
    marginBottom: "20px",
  }}
>

  <label
    style={{
      fontWeight: "600",
      marginRight: "10px",
    }}
  >
    Select Dataset:
  </label>

  <select
    value={selectedDataset || ""}
    onChange={
      handleDatasetChange
    }
    style={{
      padding: "10px 14px",
      borderRadius: "10px",
      border: "1px solid #ccc",
      fontSize: "15px",
      background: "white",
    }}
  >

    {datasets.map((dataset) => (

      <option
        key={dataset.id}
        value={dataset.id}
      >
        {dataset.name}
      </option>
    ))}

  </select>

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