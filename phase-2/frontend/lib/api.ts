/**
 * API Client Utility
 * Handles authenticated requests to FastAPI backend
 *
 * Works with Railway backend & CORS-enabled frontend.
 */

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export interface ApiRequestOptions extends RequestInit {
  requiresAuth?: boolean;
}

export async function apiRequest(
  endpoint: string,
  options: ApiRequestOptions = {}
): Promise<Response> {
  const { requiresAuth = true, headers = {}, ...fetchOptions } = options;

  const requestHeaders: Record<string, string> = {
    "Content-Type": "application/json",
    ...(headers as Record<string, string>),
  };

  if (requiresAuth && typeof window !== "undefined") {
    const token = localStorage.getItem("jwt_token");
    const expiry = localStorage.getItem("token_expiry");

    if (token && expiry) {
      const expiryTime = parseInt(expiry, 10);
      if (Date.now() < expiryTime) {
        requestHeaders["Authorization"] = `Bearer ${token}`;
      } else {
        localStorage.removeItem("jwt_token");
        localStorage.removeItem("token_expiry");
        window.location.href = "/login";
        throw new Error("Token expired");
      }
    } else if (requiresAuth) {
      window.location.href = "/login";
      throw new Error("Authentication required");
    }
  }

  const response = await fetch(`${API_URL}${endpoint}`, {
    ...fetchOptions,
    headers: requestHeaders,
  });

  if (response.status === 401 && typeof window !== "undefined") {
    localStorage.removeItem("jwt_token");
    localStorage.removeItem("token_expiry");
    window.location.href = "/login";
    throw new Error("Unauthorized");
  }

  return response;
}

export async function apiGet(endpoint: string, requiresAuth = true): Promise<Response> {
  return apiRequest(endpoint, { method: "GET", requiresAuth });
}

export async function apiPost(
  endpoint: string,
  body?: any,
  requiresAuth = true
): Promise<Response> {
  return apiRequest(endpoint, {
    method: "POST",
    body: body ? JSON.stringify(body) : undefined,
    requiresAuth,
  });
}

export async function apiPut(
  endpoint: string,
  body?: any,
  requiresAuth = true
): Promise<Response> {
  return apiRequest(endpoint, {
    method: "PUT",
    body: body ? JSON.stringify(body) : undefined,
    requiresAuth,
  });
}

export async function apiDelete(endpoint: string, requiresAuth = true): Promise<Response> {
  return apiRequest(endpoint, { method: "DELETE", requiresAuth });
}
