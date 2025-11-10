/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,

  // Static export: `next build` will write your site to ./out
  // (ideal for Cloudflare Pages static hosting)
  output: 'export',

  // If you ever use <Image/>, disable server-side optimization for static hosting
  images: { unoptimized: true },

  // Keep clean URLs (set to true only if your host requires trailing slashes)
  trailingSlash: false,
};

export default nextConfig;
