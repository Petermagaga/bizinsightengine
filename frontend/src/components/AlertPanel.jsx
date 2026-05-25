function AlertsPanel({
  alerts,
}) {
  const getColor = (
    type
  ) => {
    switch (type) {
      case "success":
        return "#16a34a";

      case "warning":
        return "#f59e0b";

      case "error":
        return "#dc2626";

      default:
        return "#6b7280";
    }
  };

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
        AI Alerts
      </h2>

      {alerts?.map(
        (alert, index) => (
          <div
            key={index}
            style={{
              borderLeft:
                `6px solid ${getColor(alert.type)}`,
              background:
                "#f9fafb",
              padding: "15px",
              marginBottom:
                "12px",
              borderRadius:
                "10px",
            }}
          >
            <strong>
              {alert.type.toUpperCase()}
            </strong>

            <p>
              {alert.message}
            </p>
          </div>
        )
      )}
    </div>
  );
}

export default AlertsPanel;