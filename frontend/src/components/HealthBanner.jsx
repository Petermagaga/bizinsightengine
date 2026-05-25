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

      case "Fair":
        return "#f59e0b";

      case "Poor":
        return "#dc2626";

      default:
        return "#6b7280";
    }
  };

  return (
    <div
      style={{
        background: getColor(),
        color: "white",
        padding: "25px",
        borderRadius: "16px",
        marginTop: "20px",
        boxShadow:
          "0 4px 12px rgba(0,0,0,0.15)",
      }}
    >
      <h2
        style={{
          margin: 0,
        }}
      >
        Business Health:
        {" "}
        {health}
      </h2>

      <p
        style={{
          marginTop: "10px",
          fontSize: "16px",
        }}
      >
        {
          summary?.headline
        }
      </p>
    </div>
  );
}

export default HealthBanner;