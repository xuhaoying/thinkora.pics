import type { Metadata } from 'next';
import Link from 'next/link';
import './globals.css';

export const metadata: Metadata = {
  title: 'Thinkora Pics - Premium Transparent PNG Images',
  description: 'Discover over 4,000 high-quality PNG images with transparent backgrounds. Perfect for designers, developers, and content creators.',
  keywords: 'transparent png, png images, transparent background, stock photos, free images, design resources',
  openGraph: {
    title: 'Thinkora Pics - Premium Transparent PNG Images',
    description: 'Discover over 4,000 high-quality PNG images with transparent backgrounds.',
    url: 'https://thinkora.pics',
    siteName: 'Thinkora Pics',
    type: 'website',
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="h-full">
      <body className="h-full bg-white dark:bg-gray-900">
        {/* Navigation */}
        <nav className="sticky top-0 z-50 bg-white/80 dark:bg-gray-900/80 backdrop-blur-lg border-b border-gray-200 dark:border-gray-800">
          <div className="container mx-auto px-4">
            <div className="flex items-center justify-between h-16">
              <Link href="/" className="flex items-center space-x-2">
                <div className="w-8 h-8 bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg"></div>
                <span className="text-xl font-bold text-gray-900 dark:text-white">Thinkora Pics</span>
              </Link>
              
              <div className="flex items-center space-x-6">
                <Link href="/" className="text-gray-600 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white transition-colors">
                  Browse
                </Link>
                <Link href="/about" className="text-gray-600 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white transition-colors">
                  About
                </Link>
                <a
                  href="https://github.com/xuhaoying/thinkora.pics"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-gray-600 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white transition-colors"
                >
                  GitHub
                </a>
              </div>
            </div>
          </div>
        </nav>
        
        {/* Main Content */}
        <div className="flex-1">
          {children}
        </div>
        
        {/* Footer */}
        <footer className="bg-gray-50 dark:bg-gray-800 border-t border-gray-200 dark:border-gray-700">
          <div className="container mx-auto px-4 py-8">
            <div className="text-center text-gray-600 dark:text-gray-400">
              <p>© 2025 Thinkora Pics. All images are provided under their respective licenses.</p>
              <p className="mt-2">
                Built with <span className="text-red-500">❤️</span> using Next.js and Cloudflare R2
              </p>
            </div>
          </div>
        </footer>
      </body>
    </html>
  );
} 