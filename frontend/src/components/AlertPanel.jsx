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

      {alerts?.map((alert, index) => (

        <div
          key={alert?.id || index}
          className="alert-card"
        >

          <h4>
            {(alert?.level || "info").toUpperCase()}
          </h4>

          <p>
            {alert?.message || "No message"}
          </p>

        </div>
      ))}


    </div>
  );
}

export default AlertsPanel;