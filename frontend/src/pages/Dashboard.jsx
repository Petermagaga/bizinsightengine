import { useEffect, useState }
from "react";

import AlertsPanel from "../components/AlertPanel";
import RecommendationsPanel from "../components/RecommendationsPanel";
import {
  getDashboard
} from "../api/dashboardApi";
import { useNavigate } from "react-router-dom";
import { getDatasets } from "../api/datasetApi";
import DecisionsPanel from "../components/DecisionsPanel";
import KPICards
from "../components/KPISection";

import ForecastChart from "../components/ForecastChart";
import TimeSeriesInsights from "../components/TimeSeriesChart";
import HealthBanner
from "../components/HealthBanner";
import DatasetChat from "../components/DatasetChat";
import ProductionChart from "../components/ProductionChart";
import SummaryCard from "../components/SummaryCard";

function Dashboard() {

  const [dashboard, setDashboard] =
    useState(null);

  const [loading, setLoading] =
    useState(true);
  const [error, setError] =
  useState(null);

  const [datasets, setDatasets] =
    useState([]);

  const [selectedDataset, setSelectedDataset] =
    useState(null);

  const navigate =
    useNavigate();
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
          navigate("/upload");
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
        setError(
          error.response?.data?.error ||
          "Failed To Load dashboard"
        )

      } finally {

        setLoading(false);
      }
    };

    fetchDashboard();

  }, []);

  const handleLogout = () => {

    localStorage.removeItem(
      "access_token"
    );

    localStorage.removeItem(
      "refresh_token"
    );

    window.location.href = "/";
  };



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

      setError(
        error.response?.data?.error ||
        "Failed to load dashboard"
      );

    } finally {

      setLoading(false);
    }
  };

  if (loading) {
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


  if (error) {
    return (
      <div
        style={{
          padding: "40px",
          color: "red",
          fontWeight: "bold",
        }}
      >
        {error}
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
    display: "flex",
    gap: "12px",
    marginTop: "20px",
    marginBottom: "20px",
  }}
>

  <button
    onClick={() => navigate("/upload")}
    style={{
      padding: "10px 18px",
      borderRadius: "10px",
      border: "none",
      background: "#2563eb",
      color: "white",
      fontWeight: "600",
      cursor: "pointer",
    }}
  >
    Upload New Dataset
  </button>


  <button
    onClick={handleLogout}
    style={{
      padding: "10px 18px",
      borderRadius: "10px",
      border: "none",
      background: "#ef4444",
      color: "white",
      fontWeight: "600",
      cursor: "pointer",
    }}
  >
    Logout
  </button>

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
      <DatasetChat
      datasetId={
        selectedDataset
      }
      />

  </div>
  </div>
);
}

export default Dashboard;