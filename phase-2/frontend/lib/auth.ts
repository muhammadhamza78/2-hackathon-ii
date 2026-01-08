/**
 * Authentication Client
 * Handles user login and token management
 */

import { apiPost } from "@/lib/api";
import type { User } from "@/types/auth";

export interface LoginResponse {
  access_token: string;
  token_type: string;
  expires_in: number;
  user: {
    id: number;
    email: string;
    name: string | null;
    profile_picture: string | null;
  };
}

export async function loginUser(email: string, password: string): Promise<LoginResponse> {
  const res = await apiPost("/api/auth/login", { email, password }, false);

  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err?.detail || "Login failed");
  }

  const data: LoginResponse = await res.json();

  if (typeof window !== "undefined") {
    // Store JWT token and expiry
    localStorage.setItem("jwt_token", data.access_token);
    const expiryTime = Date.now() + data.expires_in * 1000;
    localStorage.setItem("token_expiry", expiryTime.toString());

    // Store user data for quick access (optional but helpful)
    localStorage.setItem("user_data", JSON.stringify({
      id: data.user.id,
      email: data.user.email,
      name: data.user.name,
      profile_picture: data.user.profile_picture
    }));
  }

  return data;
}
