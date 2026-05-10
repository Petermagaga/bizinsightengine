import { useState } from "react";
import api from "../services/api";

export default function UploadModal({ onClose, refreshDatasets }) {
  const [name, setName] = useState("");
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleUpload = async () => {
    if (!file || !name) {
      alert("Please fill all fields");
      return;
    }

    try {
      setLoading(true);

      const formData = new FormData();

      formData.append("name", name);
      formData.append("file", file);

      await api.post("/data/upload/", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });

      refreshDatasets();
      onClose();

    } catch (error) {
      console.log(error);
      alert("Upload failed");

    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 bg-black/40 flex items-center justify-center z-50">

      <div className="bg-white p-6 rounded-2xl shadow-xl w-[450px]">

        <h2 className="text-2xl font-bold mb-4">
          Upload Dataset
        </h2>

        <input
          placeholder="Dataset Name"
          className="border w-full p-3 rounded-lg mb-4"
          onChange={(e) => setName(e.target.value)}
        />

        <input
          type="file"
          className="mb-4"
          onChange={(e) => setFile(e.target.files[0])}
        />

        <div className="flex justify-end gap-3">

          <button
            onClick={onClose}
            className="px-4 py-2 border rounded-lg"
          >
            Cancel
          </button>

          <button
            onClick={handleUpload}
            disabled={loading}
            className="bg-blue-500 text-white px-4 py-2 rounded-lg"
          >
            {loading ? "Uploading..." : "Upload"}
          </button>

        </div>

      </div>

    </div>
  );
}