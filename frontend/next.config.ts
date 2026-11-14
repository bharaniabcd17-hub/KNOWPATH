import type { NextConfig } from "next";

const isExport = process.env.NEXT_EXPORT === "true";

const nextConfig: NextConfig = {
  reactStrictMode: true,
  output: isExport ? "export" : undefined,
  basePath: isExport ? "/KNOWPATH" : "",
  trailingSlash: isExport ? true : false,
  images: {
    unoptimized: true,
    remotePatterns: [
      {
        protocol: "https",
        hostname: "*.supabase.co",
      },
    ],
  },
};

export default nextConfig;
