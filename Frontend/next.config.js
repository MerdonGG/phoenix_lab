/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  // Переменные окружения для клиентской части
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000',
  },
  // Настройки для работы с изображениями
  images: {
    domains: [
      'localhost',
      'images.unsplash.com',
      'source.unsplash.com',
      'www.pexels.com',
      'images.pexels.com',
    ],
    remotePatterns: [
      {
        protocol: 'https',
        hostname: '**',
      },
      {
        protocol: 'http',
        hostname: 'localhost',
        port: '5000',
      },
    ],
  },
  // Настройки для работы с API (если нужно проксирование)
  async rewrites() {
    return [
      // Раскомментируйте, если хотите проксировать API запросы через Vercel
      // {
      //   source: '/api/:path*',
      //   destination: `${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000'}/api/:path*`,
      // },
    ]
  },
}

module.exports = nextConfig

