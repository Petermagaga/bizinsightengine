export default function InsightCard({ insight }) {
  return (
    <div className="p-4 bg-white shadow mb-4">
      <h2 className="font-bold">AI Summary</h2>
      <p>{insight.summary_text}</p>

      <h3 className="mt-2 font-semibold">BI Insights</h3>
      <pre>{JSON.stringify(insight.bi_insights, null, 2)}</pre>

      <h3 className="mt-2 font-semibold">Predictions</h3>
      <pre>{JSON.stringify(insight.predictions, null, 2)}</pre>
    </div>
  );
}