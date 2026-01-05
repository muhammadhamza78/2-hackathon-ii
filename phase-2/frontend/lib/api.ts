// /**
//  * API Client Utility
//  * Handles authenticated requests to FastAPI backend
//  *
//  * Spec Reference:
//  * - specs/features/authentication.md (FR3 - JWT Token Validation)
//  * - specs/features/plans/authentication-plan.md (Section 3.3)
//  */

// const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

// export interface ApiRequestOptions extends RequestInit {
//   requiresAuth?: boolean;
// }

// /**
//  * Make an authenticated API request
//  * Automatically includes JWT token from localStorage
//  *
//  * @param endpoint - API endpoint (e.g., "/api/tasks")
//  * @param options - Fetch options with optional requiresAuth flag
//  * @returns Response object
//  */
// export async function apiRequest(
//   endpoint: string,
//   options: ApiRequestOptions = {}
// ): Promise<Response> {
//   const { requiresAuth = true, headers = {}, ...fetchOptions } = options;

//   // Build headers
//   const requestHeaders: Record<string, string> = {
//     "Content-Type": "application/json",
//     ...(headers as Record<string, string>),
//   };

//   // Add Authorization header if JWT token exists
//   if (requiresAuth && typeof window !== "undefined") {
//     const token = localStorage.getItem("jwt_token");
//     const expiry = localStorage.getItem("token_expiry");

//     // Check if token exists and is not expired
//     if (token && expiry) {
//       const expiryTime = parseInt(expiry, 10);
//       if (Date.now() < expiryTime) {
//         requestHeaders["Authorization"] = `Bearer ${token}`;
//       } else {
//         // Token expired - clear it and redirect to login
//         localStorage.removeItem("jwt_token");
//         localStorage.removeItem("token_expiry");
//         window.location.href = "/";
//         throw new Error("Token expired");
//       }
//     } else if (requiresAuth) {
//       // No token but auth required - redirect to login
//       window.location.href = "/";
//       throw new Error("Authentication required");
//     }
//   }

//   // Make request
//   const response = await fetch(`${API_URL}${endpoint}`, {
//     ...fetchOptions,
//     headers: requestHeaders,
//   });

//   // Handle 401 Unauthorized globally
//   if (response.status === 401 && typeof window !== "undefined") {
//     localStorage.removeItem("jwt_token");
//     localStorage.removeItem("token_expiry");
//     window.location.href = "/";
//     throw new Error("Unauthorized");
//   }

//   return response;
// }

// /**
//  * Convenience method for GET requests
//  */
// export async function apiGet(endpoint: string, requiresAuth = true): Promise<Response> {
//   return apiRequest(endpoint, { method: "GET", requiresAuth });
// }

// /**
//  * Convenience method for POST requests
//  */
// export async function apiPost(
//   endpoint: string,
//   body?: any,
//   requiresAuth = true
// ): Promise<Response> {
//   return apiRequest(endpoint, {
//     method: "POST",
//     body: body ? JSON.stringify(body) : undefined,
//     requiresAuth,
//   });
// }

// /**
//  * Convenience method for PUT requests
//  */
// export async function apiPut(
//   endpoint: string,
//   body?: any,
//   requiresAuth = true
// ): Promise<Response> {
//   return apiRequest(endpoint, {
//     method: "PUT",
//     body: body ? JSON.stringify(body) : undefined,
//     requiresAuth,
//   });
// }

// /**
//  * Convenience method for DELETE requests
//  */
// export async function apiDelete(endpoint: string, requiresAuth = true): Promise<Response> {
//   return apiRequest(endpoint, { method: "DELETE", requiresAuth });
// }










import { apiPost } from "@/lib/api";

export interface LoginResponse {
  access_token: string;
  token_type: string;
  expires_in: number; // in seconds
}

/**
 * Login user with email and password
 * Stores JWT token and expiry in localStorage
 */
export async function loginUser(email: string, password: string): Promise<LoginResponse> {
  const res = await apiPost("/api/auth/login", { email, password }, false); // requiresAuth = false

  if (!res.ok) {
    throw new Error("Invalid credentials");
  }

  const data: LoginResponse = await res.json();

  // Save token and expiry in localStorage
  if (typeof window !== "undefined") {
    localStorage.setItem("jwt_token", data.access_token);
    const expiryTime = Date.now() + data.expires_in * 1000; // convert seconds to ms
    localStorage.setItem("token_expiry", expiryTime.toString());
  }

  return data;
}
