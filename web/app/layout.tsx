import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Chipmunks",
  description: "Cute little inventory manager",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
