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

  const [loading, setLoading] =
    useState(false);

  const handleLogin =
    async (e) => {

      e.preventDefault();

      setLoading(true);
      setError("");

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
          "Invalid username or password"
        );

      } finally {

        setLoading(false);
      }
    };

  return (

    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-100 via-blue-50 to-slate-200 p-6">

      <div className="w-full max-w-md bg-white/90 backdrop-blur-xl rounded-3xl shadow-2xl border border-white/40 p-8">

        <div className="text-center">

          <div className="w-16 h-16 mx-auto rounded-2xl bg-blue-600 flex items-center justify-center text-white text-2xl font-bold shadow-lg">
            AI
          </div>

          <h1 className="text-4xl font-extrabold mt-6 text-slate-800">
            Welcome Back
          </h1>

          <p className="mt-2 text-slate-500">
            Sign in to access your AI dashboard
          </p>

        </div>

        <form
          onSubmit={handleLogin}
          className="mt-8 space-y-5"
        >

          <div>

            <label className="block text-sm font-semibold text-slate-700 mb-2">
              Username
            </label>

            <input
              type="text"
              placeholder="Enter username"
              className="w-full border border-slate-200 bg-slate-50 px-4 py-3 rounded-xl outline-none focus:ring-4 focus:ring-blue-200 focus:border-blue-500 transition-all"
              value={username}
              onChange={(e) =>
                setUsername(
                  e.target.value
                )
              }
            />

          </div>

          <div>

            <label className="block text-sm font-semibold text-slate-700 mb-2">
              Password
            </label>

            <input
              type="password"
              placeholder="Enter password"
              className="w-full border border-slate-200 bg-slate-50 px-4 py-3 rounded-xl outline-none focus:ring-4 focus:ring-blue-200 focus:border-blue-500 transition-all"
              value={password}
              onChange={(e) =>
                setPassword(
                  e.target.value
                )
              }
            />

          </div>

          {error && (

            <div className="bg-red-50 border border-red-200 text-red-600 px-4 py-3 rounded-xl text-sm">
              {error}
            </div>
          )}

          <button
            disabled={loading}
            className="w-full bg-blue-600 hover:bg-blue-700 text-white py-3 rounded-xl font-semibold shadow-lg transition-all duration-200 disabled:opacity-50"
          >

            {loading
              ? "Signing In..."
              : "Login"}

          </button>

        </form>

        <p className="text-center text-sm text-slate-400 mt-6">
          Gagamatrix Engine © 2026
        </p>

      </div>

    </div>
  );
}

export default Login;