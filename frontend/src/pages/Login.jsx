import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { loginUser }
from "../api/authApi";

function Login() {

  const navigate =
    useNavigate();

  const [username, setUsername] =
    useState("");

  const [password, setPassword] =
    useState("");

  const [error, setError] =
    useState("");

  const handleLogin =
    async (e) => {

      e.preventDefault();

      try {

        const data =
          await loginUser(
            username,
            password
          );

        localStorage.setItem(
          "access_token",
          data.access
        );

        localStorage.setItem(
          "refresh_token",
          data.refresh
        );

        navigate("/dashboard");

      } catch {

        setError(
          "Invalid credentials"
        );
      }
    };

  return (
    <div className="min-h-screen flex items-center justify-center bg-slate-100">

      <div className="bg-white p-8 rounded-2xl shadow-lg w-[400px]">

        <h1 className="text-3xl font-bold text-center">
          Login
        </h1>

        <form
          onSubmit={handleLogin}
          className="mt-6"
        >

          <input
            type="text"
            placeholder="Username"
            className="w-full border p-3 rounded-lg mb-4"
            value={username}
            onChange={(e) =>
              setUsername(
                e.target.value
              )
            }
          />

          <input
            type="password"
            placeholder="Password"
            className="w-full border p-3 rounded-lg mb-4"
            value={password}
            onChange={(e) =>
              setPassword(
                e.target.value
              )
            }
          />

          {error && (
            <p className="text-red-500 mb-4">
              {error}
            </p>
          )}

          <button
            className="w-full bg-blue-600 text-white py-3 rounded-lg"
          >
            Login
          </button>

        </form>
      </div>
    </div>
  );
}

export default Login;