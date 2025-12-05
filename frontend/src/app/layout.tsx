import type { Metadata } from "next";
import "./globals.css";
import Navbar from "@/components/Navigation/Navbar";

export const metadata: Metadata = {
  title: "RAG Application",
  description: "Retrieval Augmented Generation",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="min-h-screen bg-gray-50 text-gray-900">
        <Navbar />
        <main className="container mx-auto py-8 px-4">
          {children}
        </main>
      </body>
    </html>
  );
}