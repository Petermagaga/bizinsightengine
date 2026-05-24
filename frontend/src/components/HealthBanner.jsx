function HealthBanner({
  health,
  summary,
}) {
  const getColor = () => {
    switch (health) {
      case "Excellent":
        return "#16a34a";

      case "Good":
        return "#2563eb";

      case "Warning":
        return "#f59e0b";

      case "Critical":
        return "#dc2626";

      default:
        return "#6b7280";
    }
  };

  return (
    <div
      style={{
        background: "#fff",
        borderLeft: `8px solid ${getColor()}`,
        borderRadius: "16px",
        padding: "24px",
        marginBottom: "30px",
        boxShadow:
          "0 2px 10px rgba(0,0,0,0.08)",
      }}
    >
      <h2
        style={{
          color: getColor(),
          marginBottom: "10px",
        }}
      >
        {health}
      </h2>

      <h3>
        {summary.headline}
      </h3>

      <p
        style={{
          color: "#555",
        }}
      >
        {summary.key_takeaway}
      </p>
    </div>
  );
}

export default HealthBanner;