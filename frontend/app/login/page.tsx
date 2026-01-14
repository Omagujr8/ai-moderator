"use client";

import { useState } from "react";
import { login } from "@/lib/auth";

export default function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  async function handleLogin() {
    await login(email, password);
    window.location.href = "/dashboard";
  }

  return (
    <div className="flex h-screen items-center justify-center">
      <div className="w-96 space-y-4">
        <h1 className="text-2xl font-bold">Admin Login</h1>

        <input
          className="w-full border p-2"
          placeholder="Email"
          onChange={e => setEmail(e.target.value)}
        />

        <input
          className="w-full border p-2"
          type="password"
          placeholder="Password"
          onChange={e => setPassword(e.target.value)}
        />

        <button
          className="w-full bg-black text-white p-2"
          onClick={handleLogin}
        >
          Login
        </button>
      </div>
    </div>
  );
}
