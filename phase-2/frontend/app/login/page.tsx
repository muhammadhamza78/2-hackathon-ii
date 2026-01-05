"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { loginUser } from "@/lib/api";

export default function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const router = useRouter();

  const handleLogin = async () => {
    if (!email || !password) {
      setError("Please fill all fields");
      return;
    }

    setLoading(true);
    setError("");

    try {
      const data = await loginUser(email, password);

      // Save token and expiry (already done in loginUser)
      // localStorage.setItem("jwt_token", data.access_token);
      // const expiryTime = Date.now() + data.expires_in * 1000;
      // localStorage.setItem("token_expiry", expiryTime.toString());

      // Redirect to tasks page
      router.push("/tasks");
    } catch (err: any) {
      setError(err.message || "Login failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: 400, margin: "50px auto", padding: 20 }}>
      <h1>Login</h1>

      <input
        type="email"
        placeholder="Email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        style={{ display: "block", width: "100%", margin: "10px 0", padding: 8 }}
      />

      <input
        type="password"
        placeholder="Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        style={{ display: "block", width: "100%", margin: "10px 0", padding: 8 }}
      />

      <button
        onClick={handleLogin}
        disabled={loading}
        style={{ width: "100%", padding: 10, marginTop: 10 }}
      >
        {loading ? "Logging in..." : "Login"}
      </button>

      {error && <p style={{ color: "red", marginTop: 10 }}>{error}</p>}
    </div>
  );
}
