import { useEffect, useState }
from "react";

import {
  getDashboard
} from "../api/dashboardApi";

function Dashboard() {

  const [dashboard, setDashboard] =
    useState(null);

  const [loading, setLoading] =
    useState(true);

  const [error, setError] =
    useState(null);

  useEffect(() => {

    const loadDashboard =
      async () => {

      try {

        const data =
          await getDashboard(41);

        setDashboard(data);

      } catch (err) {

        setError(
          "Failed to load dashboard"
        );

      } finally {

        setLoading(false);
      }
    };

    loadDashboard();

  }, []);

  if (loading) {
    return (
      <div className="p-8">
        Loading dashboard...
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-8 text-red-500">
        {error}
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-100 p-8">

      <h1 className="text-4xl font-bold">
        AI Insights Dashboard
      </h1>

      <p className="mt-3">
        Business Health:
        <span className="font-bold ml-2">
          {
            dashboard
            .business_health
          }
        </span>
      </p>

      <div className="mt-6 bg-white rounded-xl p-6 shadow">

        <h2 className="text-xl font-bold">
          KPIs
        </h2>

        <pre className="mt-4 overflow-auto">
          {
            JSON.stringify(
              dashboard.kpis,
              null,
              2
            )
          }
        </pre>

      </div>
    </div>
  );
}

export default Dashboard;