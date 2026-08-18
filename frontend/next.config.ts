import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  reactStrictMode: true,
  skipTrailingSlashRedirect: true,
  typescript: { ignoreBuildErrors: true },
  images: { unoptimized: true },
  async rewrites() {
    const apiOrigin = process.env.DJANGO_API_ORIGIN || "http://127.0.0.1:8000";
    return [
      { source: "/api/backend/:path*", destination: `${apiOrigin}/api/:path*` },
      { source: "/media/:path*", destination: `${apiOrigin}/media/:path*` },
    ];
  },
};

export default nextConfig;
