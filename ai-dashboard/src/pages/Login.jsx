import { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../services/api";

export default function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const navigate = useNavigate();

  const handleLogin = async () => {
    try {
      const res = await api.post("/auth/login/", {
        username,
        password,
      });

      console.log(res.data);

      localStorage.setItem("access", res.data.access);
      localStorage.setItem("refresh", res.data.refresh);

      navigate("/Dashboard");
    } catch (error) {
      console.log(error);

      if (error.response) {
        alert(error.response.data.detail || "Login failed");
      } else {
        alert("Server error");
      }
    }
  };

  return (
    <div className="flex h-screen items-center justify-center">
      <div className="p-6 bg-white shadow rounded w-80">
        <h2 className="text-xl mb-4">Login</h2>

        <input
          placeholder="Username"
          className="border p-2 w-full mb-2"
          onChange={(e) => setUsername(e.target.value)}
        />

        <input
          type="password"
          placeholder="Password"
          className="border p-2 w-full mb-2"
          onChange={(e) =>  setPassword(e.target.value)}
        />



        <button
          onClick={handleLogin}
          className="bg-blue-500 text-white p-2 w-full"
        >
          Login
        </button>
      </div>
    </div>
  );
}