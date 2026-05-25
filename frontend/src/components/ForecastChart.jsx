import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
} from "recharts";

function ForecastChart({
  forecastData,
}) {
  return (
    <div
      style={{
        background: "#fff",
        padding: "20px",
        borderRadius: "16px",
        marginTop: "20px",
        boxShadow:
          "0 2px 10px rgba(0,0,0,0.08)",
      }}
    >
      <h2>
        Forecast Predictions
      </h2>

      <ResponsiveContainer
        width="100%"
        height={400}
      >
        <BarChart
          data={forecastData}
        >
          <CartesianGrid strokeDasharray="3 3" />

          <XAxis
            dataKey="label"
            angle={-20}
            textAnchor="end"
            interval={0}
            height={120}
          />

          <YAxis />

          <Tooltip />

          <Bar
            dataKey="prediction"
            fill="#2563eb"
          />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}

export default ForecastChart;