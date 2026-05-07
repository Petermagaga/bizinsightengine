import { useEffect, useState } from "react";
import api from "../services/api";

export default function ProgressBar({ datasetId }) {
  const [progress, setProgress] = useState(0);
  const [status, setStatus] = useState("");

  useEffect(() => {
    const interval = setInterval(async () => {
      const res = await api.get(`/data/${datasetId}/status/`);
      setProgress(res.data.progress);
      setStatus(res.data.status);
    }, 2000);

    return () => clearInterval(interval);
  }, [datasetId]);

  return (
    <div>
      <p>{status}</p>
      <div className="w-full bg-gray-200 h-4">
        <div
          className="bg-blue-500 h-4"
          style={{ width: `${progress}%` }}
        ></div>
      </div>
    </div>
  );
}