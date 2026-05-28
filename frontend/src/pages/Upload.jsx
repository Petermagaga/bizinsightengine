import {
  useState,
  useEffect
} from "react";

import {
  useNavigate
} from "react-router-dom";

import {
  uploadDataset,
  getDatasetStatus
} from "../api/uploadApi";

function Upload() {

  const navigate =
    useNavigate();

  const [file, setFile] =
    useState(null);

  const [name, setName] =
    useState("");

  const [loading, setLoading] =
    useState(false);

  const [datasetId, setDatasetId] =
    useState(null);

  const [status, setStatus] =
    useState("");

  const [progress, setProgress] =
    useState(0);

  const handleUpload =
    async () => {

    if (!file || !name) {
      return;
    }

    try {

      setLoading(true);

      const formData =
        new FormData();

      formData.append(
        "name",
        name
      );

      formData.append(
        "file",
        file
      );

      const res =
        await uploadDataset(
          formData
        );

      setDatasetId(
        res.dataset_id
      );

      setStatus(
        "processing"
      );

    } catch (err) {

      console.log(
        err.response?.data
      );

      setLoading(false);
    }
  };

  useEffect(() => {

    if (!datasetId) return;

    const interval =
      setInterval(
        async () => {

        try {

          const data =
            await getDatasetStatus(
              datasetId
            );

          setProgress(
            data.progress
          );

          setStatus(
            data.status
          );

          if (
            data.status ===
            "completed"
          ) {

            clearInterval(
              interval
            );

            navigate(
              "/dashboard"
            );
          }

        } catch (error) {

          console.error(error);
        }
      }, 3000);

    return () =>
      clearInterval(interval);

  }, [datasetId]);

  return (

    <div
      style={{
        minHeight: "100vh",
        display: "flex",
        justifyContent:
          "center",
        alignItems:
          "center",
        background:
          "#f5f7fb",
        padding: "20px",
      }}
    >

      <div
        className="card"
        style={{
          width: "500px",
        }}
      >

        <h1
          style={{
            fontSize: "32px",
            fontWeight: "700",
            marginBottom: "10px",
          }}
        >
          Upload Dataset
        </h1>

        <p
          style={{
            color: "#6b7280",
            marginBottom: "30px",
          }}
        >
          Upload CSV or Excel
          dataset for AI analysis
        </p>

        <input
          type="text"
          placeholder="Dataset name"
          value={name}
          onChange={(e) =>
            setName(
              e.target.value
            )
          }
          style={{
            width: "100%",
            padding: "14px",
            marginBottom: "20px",
            borderRadius: "10px",
            border:
              "1px solid #ddd",
          }}
        />

        <input
          type="file"
          onChange={(e) =>
            setFile(
              e.target.files[0]
            )
          }
          style={{
            marginBottom: "20px",
          }}
        />

        <button
          onClick={handleUpload}
          disabled={loading}
          style={{
            width: "100%",
            padding: "14px",
            borderRadius: "12px",
            border: "none",
            background:
              "#2563eb",
            color: "white",
            fontWeight: "600",
            cursor: "pointer",
          }}
        >

          {loading
            ? "Uploading..."
            : "Upload Dataset"}

        </button>

        {status && (

          <div
            style={{
              marginTop: "25px",
            }}
          >

            <p>
              Status:
              <strong>
                {" "}
                {status}
              </strong>
            </p>

            <div
              style={{
                width: "100%",
                height: "12px",
                background:
                  "#e5e7eb",
                borderRadius: "999px",
                overflow: "hidden",
                marginTop: "10px",
              }}
            >

              <div
                style={{
                  width:
                    `${progress}%`,
                  height: "100%",
                  background:
                    "#2563eb",
                }}
              />

            </div>

            <p
              style={{
                marginTop: "10px",
              }}
            >
              {progress}% completed
            </p>

          </div>
        )}

      </div>

    </div>
  );
}

export default Upload;