import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";

import DashboardLayout from "../layouts/DashboardLayout";

import api from "../services/api";

import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  PieChart,
  Pie,
  LineChart,
  Line,
} from "recharts";

export default function AnalyticsPage() {

  const { id } = useParams();

  const [dataset, setDataset] = useState(null);
  const [analysis, setAnalysis] = useState(null);
  const [insights, setInsights] = useState([]);

  const fetchData = async () => {
    try {

      const datasetRes = await api.get(`/data/${id}/status/`);

      setDataset(datasetRes.data);

      const analysisRes = await api.get(`/analytics/${id}/`);

      setAnalysis(analysisRes.data);

      const insightsRes = await api.get(`/insights/${id}/`);

      setInsights(insightsRes.data);

    } catch (error) {
      console.log(error);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const chartData = analysis?.summary?.mean
    ? Object.entries(analysis.summary.mean).map(
        ([key, value]) => ({
          name: key,
          value,
        })
      )
    : [];

  return (
    <DashboardLayout>

      {/* HEADER */}
      <div className="mb-8">

        <h1 className="text-3xl font-bold">
          {dataset?.name}
        </h1>

        <p className="text-gray-500 mt-2">
          AI-powered analytics and business insights
        </p>

      </div>

      {/* KPI SECTION */}
      <div className="grid grid-cols-4 gap-6 mb-8">

        <div className="bg-white p-6 rounded-2xl shadow">
          <p className="text-gray-500">
            Status
          </p>

          <h2 className="text-2xl font-bold mt-2">
            {dataset?.status}
          </h2>
        </div>

        <div className="bg-white p-6 rounded-2xl shadow">
          <p className="text-gray-500">
            Progress
          </p>

          <h2 className="text-2xl font-bold mt-2">
            {dataset?.progress}%
          </h2>
        </div>

        <div className="bg-white p-6 rounded-2xl shadow">
          <p className="text-gray-500">
            Rows
          </p>

          <h2 className="text-2xl font-bold mt-2">
            {dataset?.processed_rows}
          </h2>
        </div>

        <div className="bg-white p-6 rounded-2xl shadow">
          <p className="text-gray-500">
            AI Insights
          </p>

          <h2 className="text-2xl font-bold mt-2">
            {insights.length}
          </h2>
        </div>

      </div>

      {/* CHARTS */}
      <div className="grid grid-cols-2 gap-6 mb-8">

        {/* BAR CHART */}
        <div className="bg-white p-6 rounded-2xl shadow">

          <h2 className="text-xl font-bold mb-4">
            Mean Values
          </h2>

          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={chartData}>
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="value" />
            </BarChart>
          </ResponsiveContainer>

        </div>

        {/* PIE CHART */}
        <div className="bg-white p-6 rounded-2xl shadow">

          <h2 className="text-xl font-bold mb-4">
            Distribution
          </h2>

          <ResponsiveContainer width="100%" height={300}>
            <PieChart>

              <Pie
                data={chartData}
                dataKey="value"
                nameKey="name"
              />

              <Tooltip />

            </PieChart>
          </ResponsiveContainer>

        </div>

      </div>

      {/* LINE CHART */}
      <div className="bg-white p-6 rounded-2xl shadow mb-8">

        <h2 className="text-xl font-bold mb-4">
          Trend Analysis
        </h2>

        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={chartData}>

            <XAxis dataKey="name" />

            <YAxis />

            <Tooltip />

            <Line
              type="monotone"
              dataKey="value"
            />

          </LineChart>
        </ResponsiveContainer>

      </div>

      {/* AI INSIGHTS */}
      <div className="bg-white p-6 rounded-2xl shadow">

        <h2 className="text-2xl font-bold mb-6">
          AI Business Insights
        </h2>

        <div className="space-y-6">

          {insights.map((insight) => (

            <div
              key={insight.id}
              className="border rounded-xl p-5"
            >

              <p className="text-gray-700 whitespace-pre-wrap">
                {insight.summary_text}
              </p>

              {/* BI INSIGHTS */}
              {insight.bi_insights && (
                <div className="mt-4">

                  <h3 className="font-bold mb-2">
                    BI Insights
                  </h3>

                  <pre className="bg-gray-100 p-3 rounded-lg overflow-auto">
                    {JSON.stringify(
                      insight.bi_insights,
                      null,
                      2
                    )}
                  </pre>

                </div>
              )}

              {/* PREDICTIONS */}
              {insight.predictions && (
                <div className="mt-4">

                  <h3 className="font-bold mb-2">
                    Predictions
                  </h3>

                  <pre className="bg-gray-100 p-3 rounded-lg overflow-auto">
                    {JSON.stringify(
                      insight.predictions,
                      null,
                      2
                    )}
                  </pre>

                </div>
              )}

            </div>

          ))}

        </div>

      </div>

    </DashboardLayout>
  );
}