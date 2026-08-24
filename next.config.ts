import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Standalone output bundles a minimal server into .next/standalone,
  // keeping the production container image small.
  output: "standalone",
};

export default nextConfig;
