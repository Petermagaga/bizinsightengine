import { Trash2 } from "lucide-react";
import api from "../services/api";

export default function DatasetTable({
  datasets,
  refreshDatasets,
}) {

  const handleDelete = async (id) => {
    try {

      await api.delete(`/data/${id}/delete/`);

      refreshDatasets();

    } catch (error) {
      console.log(error);
      alert("Delete failed");
    }
  };

  return (
    <div className="bg-white rounded-2xl shadow p-6 mt-6">

      <h2 className="text-xl font-bold mb-4">
        Uploaded Datasets
      </h2>

      <table className="w-full">

        <thead>
          <tr className="text-left border-b">
            <th className="pb-3">Name</th>
            <th>Status</th>
            <th>Progress</th>
            <th>Rows</th>
            <th>Uploaded</th>
            <th></th>
          </tr>
        </thead>

        <tbody>

          {datasets.map((dataset) => (

            <tr
              key={dataset.id}
              className="border-b hover:bg-gray-50"
            >
              <td className="py-4">
                {dataset.name}
              </td>

              <td>
                <span className={`px-3 py-1 rounded-full text-sm ${
                  dataset.status === "completed"
                    ? "bg-green-100 text-green-600"
                    : dataset.status === "failed"
                    ? "bg-red-100 text-red-600"
                    : "bg-yellow-100 text-yellow-600"
                }`}>
                  {dataset.status}
                </span>
              </td>

              <td className="w-48">

                <div className="bg-gray-200 rounded-full h-3">

                  <div
                    className="bg-blue-500 h-3 rounded-full"
                    style={{
                      width: `${dataset.progress}%`,
                    }}
                  />

                </div>

                <p className="text-sm mt-1">
                  {dataset.progress}%
                </p>

              </td>

              <td>
                {dataset.processed_rows}
              </td>

              <td>
                {new Date(
                  dataset.uploaded_at
                ).toLocaleDateString()}
              </td>

              <td>
                <button
                  onClick={() => handleDelete(dataset.id)}
                  className="text-red-500"
                >
                  <Trash2 size={18} />
                </button>
              </td>

            </tr>

          ))}

        </tbody>

      </table>

    </div>
  );
}