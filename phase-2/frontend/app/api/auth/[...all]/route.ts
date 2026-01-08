<<<<<<< HEAD
// // backend/app/api/auth/route.ts
// import { auth } from "@/lib/auth";

// // POST /api/auth → login
// export async function POST(req: Request) {
//   try {
//     const { email, password } = await req.json();
//     const data = await auth.login({ email, password });
//     return new Response(JSON.stringify(data), { status: 200 });
//   } catch (err: any) {
//     return new Response(JSON.stringify({ detail: err.message || "Login failed" }), { status: 401 });
//   }
// }
=======
import { auth } from "@/lib/auth";
import { toNextJsHandler } from "better-auth/next-js";
>>>>>>> 09fec55ab4658b42257e6db6376aa6c6353809ac

// // GET /api/auth → check session
// export async function GET(req: Request) {
//   try {
//     const token = req.headers.get("Authorization")?.replace("Bearer ", "");
//     if (!token) return new Response(JSON.stringify({ user: null }), { status: 200 });

//     const user = await auth.session({ token });
//     return new Response(JSON.stringify({ user }), { status: 200 });
//   } catch {
//     return new Response(JSON.stringify({ user: null }), { status: 200 });
//   }
// }
