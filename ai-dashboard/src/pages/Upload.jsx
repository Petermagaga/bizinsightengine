import { useState } from "react";
import api from "../services/api";

export default function Upload() {
  const [file, setFile] = useState(null);
  const [name, setName] = useState("");
  const [datasetId, setDatasetId] = useState(null);

  const handleUpload = async () => {
    try {
      const formData = new FormData();

      formData.append("name", name);
      formData.append("file", file);

      const res = await api.post(
        "/data/upload/",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );

      setDatasetId(res.data.dataset_id);

    } catch (err) {
      console.log(err.response?.data);
    }
  };

  return (
    <div className="p-6">
      <h1 className="text-2xl mb-4">Upload Dataset</h1>

      <input
        type="text"
        placeholder="Dataset name"
        value={name}
        onChange={(e) => setName(e.target.value)}
        className="border p-2 mr-2"
      />

      <input
        type="file"
        onChange={(e) => setFile(e.target.files[0])}
      />

      <button
        onClick={handleUpload}
        className="bg-green-500 text-white p-2 ml-2"
      >
        Upload
      </button>

      {datasetId && <p>Dataset ID: {datasetId}</p>}
    </div>
  );
}