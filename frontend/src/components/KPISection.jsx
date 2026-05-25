function KPICards({ kpis }) {
  return (
    <div
      style={{
        display: "grid",
        gridTemplateColumns:
          "repeat(auto-fit, minmax(220px, 1fr))",
        gap: "20px",
        marginBottom: "30px",
      }}
    >
      <div style={cardStyle}>
        <h2>{kpis.quality_score}%</h2>
        <p>Quality Score</p>
      </div>

      <div style={cardStyle}>
        <h2>{kpis.forecast_count}</h2>
        <p>Forecast Count</p>
      </div>

      <div style={cardStyle}>
        <h2>{kpis.anomalies_found}</h2>
        <p>Anomalies Found</p>
      </div>

      <div style={cardStyle}>
        <h3>{kpis.top_metric}</h3>
        <p>Top Product</p>
      </div>
    </div>
  );
}

const cardStyle = {
  background: "#fff",
  padding: "20px",
  borderRadius: "16px",
  boxShadow:
    "0 2px 10px rgba(0,0,0,0.08)",
  textAlign: "center",
};

export default KPICards;