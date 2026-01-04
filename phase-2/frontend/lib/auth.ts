const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export interface User {
  id: number;
  email: string;
}

export interface LoginResponse {
  access_token: string;
  token_type: string;
  expires_in: number;
}

export interface RegisterData {
  email: string;
  password: string;
}

export interface LoginData {
  email: string;
  password: string;
}

async function register(data: RegisterData): Promise<User> {
  const response = await fetch(`${API_URL}/api/auth/register`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || "Registration failed");
  }

  return response.json();
}

async function login(data: LoginData): Promise<LoginResponse> {
  const response = await fetch(`${API_URL}/api/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || "Login failed");
  }

  const tokenData = await response.json();

  if (typeof window !== "undefined") {
    localStorage.setItem("access_token", tokenData.access_token);
    localStorage.setItem("token_type", tokenData.token_type);
  }

  return tokenData;
}

function logout(): void {
  if (typeof window !== "undefined") {
    localStorage.removeItem("access_token");
    localStorage.removeItem("token_type");
  }
}

function getAccessToken(): string | null {
  if (typeof window !== "undefined") {
    return localStorage.getItem("access_token");
  }
  return null;
}

function isAuthenticated(): boolean {
  return getAccessToken() !== null;
}

function getAuthHeader(): Record<string, string> {
  const token = getAccessToken();
  if (token) return { Authorization: `Bearer ${token}` };
  return {};
}

export const auth = {
  register,
  login,
  logout,
  getAccessToken,
  isAuthenticated,
  getAuthHeader,
};
