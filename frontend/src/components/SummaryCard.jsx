function SummaryCard({
  summary,
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
        Executive Summary
      </h2>

      <h3
        style={{
          marginBottom: "10px",
        }}
      >
        {summary?.headline}
      </h3>

      <p
        style={{
          color: "#555",
          lineHeight: "1.6",
        }}
      >
        {summary?.key_takeaway}
      </p>
    </div>
  );
}

export default SummaryCard;