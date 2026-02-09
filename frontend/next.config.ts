import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  output: 'export',
  basePath: '/silver_report',
  images: {
    unoptimized: true,
  },
};

export default nextConfig;
