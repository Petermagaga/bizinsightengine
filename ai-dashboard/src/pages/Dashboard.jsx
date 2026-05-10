import { useEffect, useState } from "react";

import DashboardLayout from "../layouts/DashboardLayout";

import UploadModal from "../components/UploadModal";
import DatasetTable from "../components/DatasetTable";

import api from "../services/api";

export default function Dashboard() {

  const [datasets, setDatasets] = useState([]);
  const [showUpload, setShowUpload] = useState(false);

  const fetchDatasets = async () => {
    try {

      const res = await api.get("/data/");

      setDatasets(res.data);

    } catch (error) {
      console.log(error);
    }
  };

  useEffect(() => {

    fetchDatasets();

    // auto refresh every 3 sec
    const interval = setInterval(() => {
      fetchDatasets();
    }, 3000);

    return () => clearInterval(interval);

  }, []);

  return (
    <DashboardLayout>

      {/* TOP BAR */}
      <div className="flex justify-between items-center mb-6">

        <div>
          <h1 className="text-3xl font-bold">
            AI Analytics Dashboard
          </h1>

          <p className="text-gray-500 mt-1">
            Upload and analyze datasets with AI
          </p>
        </div>

        <button
          onClick={() => setShowUpload(true)}
          className="bg-blue-500 text-white px-5 py-3 rounded-xl"
        >
          Upload Dataset
        </button>

      </div>

      {/* KPI CARDS */}
      <div className="grid grid-cols-4 gap-6">

        <div className="bg-white p-6 rounded-2xl shadow">
          <p className="text-gray-500">
            Datasets
          </p>

          <h2 className="text-4xl font-bold mt-2">
            {datasets.length}
          </h2>
        </div>

        <div className="bg-white p-6 rounded-2xl shadow">
          <p className="text-gray-500">
            Completed
          </p>

          <h2 className="text-4xl font-bold mt-2">
            {
              datasets.filter(
                d => d.status === "completed"
              ).length
            }
          </h2>
        </div>

        <div className="bg-white p-6 rounded-2xl shadow">
          <p className="text-gray-500">
            Processing
          </p>

          <h2 className="text-4xl font-bold mt-2">
            {
              datasets.filter(
                d => d.status === "processing"
              ).length
            }
          </h2>
        </div>

        <div className="bg-white p-6 rounded-2xl shadow">
          <p className="text-gray-500">
            Failed
          </p>

          <h2 className="text-4xl font-bold mt-2">
            {
              datasets.filter(
                d => d.status === "failed"
              ).length
            }
          </h2>
        </div>

      </div>

      {/* DATASET TABLE */}
      <DatasetTable
        datasets={datasets}
        refreshDatasets={fetchDatasets}
      />

      {/* UPLOAD MODAL */}
      {showUpload && (
        <UploadModal
          onClose={() => setShowUpload(false)}
          refreshDatasets={fetchDatasets}
        />
      )}

    </DashboardLayout>
  );
}