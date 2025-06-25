import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'Thinkora Pics',
  description: 'High-quality PNG images with transparent backgrounds.',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
} 