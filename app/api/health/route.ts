import { NextResponse } from "next/server";
import pkg from "@/package.json";

// Liveness/readiness probe used by the container healthcheck and
// uptime monitoring. Returns the running version so deploys are traceable.
export async function GET() {
  return NextResponse.json({
    status: "ok",
    version: pkg.version,
    uptimeSeconds: Math.round(process.uptime()),
  });
}
