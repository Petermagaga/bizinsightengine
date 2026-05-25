function TimeSeriesInsights({
  timeSeries,
}) {
  const latest =
    timeSeries?.[
      timeSeries.length - 1
    ];

  const first =
    timeSeries?.[0];

  const growth =
    latest &&
    first
      ? (
          ((latest.production -
            first.production) /
            first.production) *
          100
        ).toFixed(1)
      : 0;

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
        Production Insights
      </h2>

      <p>
        Production grew by
        {" "}
        <strong>
          {growth}%
        </strong>
        {" "}
        during the tracked
        period.
      </p>

      <p>
        Latest production:
        {" "}
        <strong>
          {
            latest?.production
          }
        </strong>
      </p>
    </div>
  );
}

export default TimeSeriesInsights;