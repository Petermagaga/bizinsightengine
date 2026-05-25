function DecisionsPanel({
  decisions,
}) {
  const getColor = (
    priority
  ) => {
    switch (priority) {
      case "high":
        return "#dc2626";

      case "medium":
        return "#f59e0b";

      case "low":
        return "#16a34a";

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
        AI Decisions
      </h2>

      {decisions &&
        Object.entries(
          decisions
        ).map(
          ([key, item]) => (
            <div
              key={key}
              style={{
                borderLeft:
                  `6px solid ${getColor(item.priority)}`,
                background:
                  "#f9fafb",
                padding:
                  "16px",
                marginBottom:
                  "12px",
                borderRadius:
                  "10px",
              }}
            >
              <h4
                style={{
                  margin: 0,
                }}
              >
                {item.action}
              </h4>

              <small>
                Priority:
                {" "}
                <strong>
                  {
                    item.priority
                  }
                </strong>
              </small>

              <p>
                {
                  item.recommendation ||
                  item.recommendations
                }
              </p>
            </div>
          )
        )}
    </div>
  );
}

export default DecisionsPanel;