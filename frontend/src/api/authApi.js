import axios from "axios";

const API = axios.create({
  baseURL: "http://127.0.0.1:8000",
});

export const loginUser =
  async (username, password) => {

    const response =
      await API.post(
        "/api/token/",
        {
          username,
          password,
        }
      );

    return response.data;
};