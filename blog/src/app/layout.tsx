import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import GoogleAnalytics from "@/components/GoogleAnalytics";

const inter = Inter({
  subsets: ["latin"],
  display: 'swap',
  variable: '--font-inter',
});

// Get GA ID from environment variable
const GA_MEASUREMENT_ID = process.env.NEXT_PUBLIC_GA_MEASUREMENT_ID || 'G-FHQHV4VFGY';

export const metadata: Metadata = {
  title: "Global News 24 | Trending News",
  description: "Discover the latest trending topics and stories from around the world. Fresh content updated every hour.",
  keywords: ["trending", "news", "viral", "stories", "latest"],
  authors: [{ name: "Editorial Team" }],
  openGraph: {
    title: "Global News 24 | Trending News",
    description: "Discover the latest trending topics and stories from around the world.",
    type: "website",
    locale: "en_US",
  },
  twitter: {
    card: "summary_large_image",
    title: "Global News 24 | Trending News",
    description: "Discover the latest trending topics and stories from around the world.",
  },
  robots: {
    index: true,
    follow: true,
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className={inter.variable}>
      <head>
        <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🔥</text></svg>" />
      </head>
      <body className={`${inter.className} antialiased`}>
        <GoogleAnalytics measurementId={GA_MEASUREMENT_ID} />
        {children}
      </body>
    </html>
  );
}
