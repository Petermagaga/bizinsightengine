function KPICards({ kpis={} }) {
  const cards = [
    {
      title: "Quality Score",
      value: `${kpis?.quality_score || 0}%`,
    },
    {
      title: "Top Metric",
      value: kpis?.top_metric || "N/A",
    },
    {
      title: "Top Value",
      value: kpis?.top_value || 0,
    },
    {
      title: "Anomalies",
      value: kpis?.anomalies_found || 0,
    },
    {
      title: "Forecast Count",
      value: kpis?.forecast_count || 0,
    },
  ];
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
      {cards.map((card, index) => (
        <div
          key={index}
          style={{
            background: "white",
            padding: "25px",
            borderRadius: "18px",
            boxShadow:
              "0 4px 12px rgba(0,0,0,0.08)",
            transition: "0.3s",
          }}
        >
          <h4
            style={{
              color: "#6b7280",
              fontSize: "14px",
              marginBottom: "12px",
            }}
          >
            {card.title}
          </h4>

          <h2
            style={{
              fontSize: "24px",
              fontWeight: "bold",
              color: "#111827",
              wordBreak: "break-word",
            }}
          >
            {card.value}
          </h2>
        </div>
      ))}
    </div>
  );
}

export default KPICards;