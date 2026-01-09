// <<<<<<< HEAD
// "use client";

// import { useState } from "react";
// import { useRouter } from "next/navigation";
// import { loginUser } from "@/lib/auth";
// import Link from "next/link";

// export default function LoginPage() {
//   const [email, setEmail] = useState("");
//   const [password, setPassword] = useState("");
//   const [error, setError] = useState("");
//   const [loading, setLoading] = useState(false);
//   const router = useRouter();

//   const handleLogin = async (e: React.FormEvent) => {
//     e.preventDefault();

//     if (!email || !password) {
//       setError("Please fill all fields");
//       // return;
//     }

//     setLoading(true);
//     setError("");

//     try {
//       await loginUser(email, password);
//       router.push("/dashboard");
//     } catch (err: any) {
//       setError(err.message || "Login failed");
//     } finally {
//       setLoading(false);
//     }
//   };

//   return (
//     <div className="min-h-screen flex items-center justify-center transition-colors" style={{ background: 'var(--background)' }}>
//       <div className="w-full max-w-md p-8 space-y-6 rounded-2xl shadow-lg transition-colors" style={{ background: 'var(--card-bg)' }}>
//         {/* Logo */}
//         <div className="text-center">
//           <h1 className="text-4xl font-bold tracking-tight mb-2">
//             <span style={{ color: 'var(--foreground)', opacity: 0.6 }}>TO</span>
//             <span className="text-[#e08b3d]">DO</span>
//             <span className="inline-flex items-center justify-center w-10 h-10 ml-1 rounded-full bg-[#e08b3d] text-white align-middle">
//               <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={3}>
//                 <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
//               </svg>
//             </span>
//           </h1>
//           <p className="text-sm" style={{ color: 'var(--foreground)', opacity: 0.6 }}>Sign in to your account</p>
//         </div>

//         {/* Login Form */}
//         <form onSubmit={handleLogin} className="space-y-4">
//           <div>
//             <label htmlFor="email" className="block text-sm font-medium mb-1" style={{ color: 'var(--foreground)' }}>
//               Email Address
//             </label>
//             <input
//               id="email"
//               type="email"
//               placeholder="you@example.com"
//               value={email}
//               onChange={(e) => setEmail(e.target.value)}
//               className="w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-[#e08b3d] focus:border-transparent transition-all"
//               style={{
//                 background: 'var(--input-bg)',
//                 color: 'var(--input-text)',
//                 borderColor: 'var(--card-border)'
//               }}
//               disabled={loading}
//             />
//           </div>

//           <div>
//             <label htmlFor="password" className="block text-sm font-medium mb-1" style={{ color: 'var(--foreground)' }}>
//               Password
//             </label>
//             <input
//               id="password"
//               type="password"
//               placeholder="••••••••"
//               value={password}
//               onChange={(e) => setPassword(e.target.value)}
//               className="w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-[#e08b3d] focus:border-transparent transition-all"
//               style={{
//                 background: 'var(--input-bg)',
//                 color: 'var(--input-text)',
//                 borderColor: 'var(--card-border)'
//               }}
//               disabled={loading}
//             />
//           </div>

//           {error && (
//             <div className="bg-red-50 dark:bg-red-900/20 border-l-4 border-red-500 p-4 rounded">
//               <p className="text-sm text-red-800 dark:text-red-400">{error}</p>
//             </div>
//           )}

//           <button
//             type="submit"
//             disabled={loading}
//             className="w-full bg-[#e08b3d] hover:bg-[#d17a2f] text-white font-semibold py-3 px-4 rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
//           >
//             {loading ? "Signing in..." : "Sign In"}
//           </button>
//         </form>

//         <p className="text-center text-sm" style={{ color: 'var(--foreground)', opacity: 0.7 }}>
//           Don't have an account?{" "}
//           <Link href="/register" className="text-[#e08b3d] hover:underline font-medium">
//             Sign up
//           </Link>
//         </p>
//       </div>
//     </div>
//   );
// }






// =======
// "use client";

// import { useState } from "react";
// import { useRouter } from "next/navigation";
// import { loginUser } from "@/lib/api";

// export default function LoginPage() {
//   const [email, setEmail] = useState("");
//   const [password, setPassword] = useState("");
//   const [error, setError] = useState("");
//   const [loading, setLoading] = useState(false);
//   const router = useRouter();

//   const handleLogin = async () => {
//     if (!email || !password) {
//       setError("Please fill all fields");
//       return;
//     }

//     setLoading(true);
//     setError("");

//     try {
//       const data = await loginUser(email, password);

//       // Save token and expiry (already done in loginUser)
//       // localStorage.setItem("jwt_token", data.access_token);
//       // const expiryTime = Date.now() + data.expires_in * 1000;
//       // localStorage.setItem("token_expiry", expiryTime.toString());

//       // Redirect to tasks page
//       router.push("/tasks");
//     } catch (err: any) {
//       setError(err.message || "Login failed");
//     } finally {
//       setLoading(false);
//     }
//   };

//   return (
//     <div style={{ maxWidth: 400, margin: "50px auto", padding: 20 }}>
//       <h1>Login</h1>

//       <input
//         type="email"
//         placeholder="Email"
//         value={email}
//         onChange={(e) => setEmail(e.target.value)}
//         style={{ display: "block", width: "100%", margin: "10px 0", padding: 8 }}
//       />

//       <input
//         type="password"
//         placeholder="Password"
//         value={password}
//         onChange={(e) => setPassword(e.target.value)}
//         style={{ display: "block", width: "100%", margin: "10px 0", padding: 8 }}
//       />

//       <button
//         onClick={handleLogin}
//         disabled={loading}
//         style={{ width: "100%", padding: 10, marginTop: 10 }}
//       >
//         {loading ? "Logging in..." : "Login"}
//       </button>

//       {error && <p style={{ color: "red", marginTop: 10 }}>{error}</p>}
//     </div>
//   );
// }
// >>>>>>> 09fec55ab4658b42257e6db6376aa6c6353809ac







"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { loginUser } from "@/lib/api";
import Link from "next/link";

export default function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const router = useRouter();

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!email || !password) {
      setError("Please fill all fields");
      return;
    }

    setLoading(true);
    setError("");

    try {
      await loginUser(email, password);
      router.push("/dashboard");
    } catch (err: any) {
      setError(err.message || "Login failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center transition-colors" style={{ background: 'var(--background)' }}>
      <div className="w-full max-w-md p-8 space-y-6 rounded-2xl shadow-lg transition-colors" style={{ background: 'var(--card-bg)' }}>

        <div className="text-center">
          <h1 className="text-4xl font-bold tracking-tight mb-2">
            <span style={{ color: 'var(--foreground)', opacity: 0.6 }}>TO</span>
            <span className="text-[#e08b3d]">DO</span>
            <span className="inline-flex items-center justify-center w-10 h-10 ml-1 rounded-full bg-[#e08b3d] text-white align-middle">
              <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={3}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
              </svg>
            </span>
          </h1>
          <p className="text-sm" style={{ color: 'var(--foreground)', opacity: 0.6 }}>Sign in to your account</p>
        </div>

        <form onSubmit={handleLogin} className="space-y-4">
          <div>
            <label htmlFor="email" className="block text-sm font-medium mb-1" style={{ color: 'var(--foreground)' }}>
              Email Address
            </label>
            <input
              id="email"
              type="email"
              placeholder="you@example.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-[#e08b3d] focus:border-transparent transition-all"
              style={{ background: 'var(--input-bg)', color: 'var(--input-text)', borderColor: 'var(--card-border)' }}
              disabled={loading}
            />
          </div>

          <div>
            <label htmlFor="password" className="block text-sm font-medium mb-1" style={{ color: 'var(--foreground)' }}>
              Password
            </label>
            <input
              id="password"
              type="password"
              placeholder="••••••••"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-[#e08b3d] focus:border-transparent transition-all"
              style={{ background: 'var(--input-bg)', color: 'var(--input-text)', borderColor: 'var(--card-border)' }}
              disabled={loading}
            />
          </div>

          {error && (
            <div className="bg-red-50 dark:bg-red-900/20 border-l-4 border-red-500 p-4 rounded">
              <p className="text-sm text-red-800 dark:text-red-400">{error}</p>
            </div>
          )}

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-[#e08b3d] hover:bg-[#d17a2f] text-white font-semibold py-3 px-4 rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {loading ? "Signing in..." : "Sign In"}
          </button>
        </form>

        <p className="text-center text-sm" style={{ color: 'var(--foreground)', opacity: 0.7 }}>
          Don't have an account?{" "}
          <Link href="/register" className="text-[#e08b3d] hover:underline font-medium">
            Sign up
          </Link>
        </p>
      </div>
    </div>
  );
}

