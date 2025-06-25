/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  images: {
    remotePatterns: [
      {
        protocol: 'https',
        hostname: 'img.thinkora.pics',
        port: '',
        pathname: '/images/**',
      },
      {
        protocol: 'https',
        hostname: 'r2.thinkora.pics',
        port: '',
        pathname: '/images/**',
      },
    ],
  },
};

export default nextConfig; 