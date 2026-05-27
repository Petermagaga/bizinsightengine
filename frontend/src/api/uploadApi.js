import axios from "axios";

const API = axios.create({
  baseURL:
    "http://127.0.0.1:8000/api/data/",
});

API.interceptors.request.use(
  (config) => {

    const token =
      localStorage.getItem(
        "access_token"
      );

    if (token) {

      config.headers.Authorization =
        `Bearer ${token}`;
    }

    return config;
  }
);

export const uploadDataset =
  async (formData) => {

    const response =
      await API.post(
        "upload/",
        formData,
        {
          headers: {
            "Content-Type":
              "multipart/form-data",
          },
        }
      );

    return response.data;
  };

export const getDatasetStatus =
  async (datasetId) => {

    const response =
      await API.get(
        `${datasetId}/status/`
      );

    return response.data;
  };