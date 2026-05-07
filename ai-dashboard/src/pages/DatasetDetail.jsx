import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import api from "../services/api";
import InsightCard from "../components/InsightCard";

export default function DatasetDetail() {
  const { id } = useParams();
  const [insights, setInsights] = useState([]);

  useEffect(() => {
    api.get(`/insights/${id}/`).then((res) => {
      setInsights(res.data);
    });
  }, [id]);

  return (
    <div className="p-6">
      <h1 className="text-2xl">Dataset Insights</h1>

      {insights.map((insight) => (
        <InsightCard key={insight.id} insight={insight} />
      ))}
    </div>
  );
}