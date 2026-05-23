import axios from "axios";

const API = axios.create({
  baseURL: "http://127.0.0.1:8000/api",
});

// Attach JWT token automatically
API.interceptors.request.use((config) => {
  const token = localStorage.getItem("access");

  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }

  return config;
});

// LOGIN
export const loginUser = async (username, password) => {
  const response = await API.post("/token/", {
    username,
    password,
  });

  return response.data;
};

export default API;