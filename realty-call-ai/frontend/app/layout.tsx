import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'RealtyCall AI - Smart Real Estate Assistant',
  description: 'AI-powered real estate sales platform with voice calls and intelligent property matching',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>
        <main className="min-h-screen">{children}</main>
      </body>
    </html>
  );
}
