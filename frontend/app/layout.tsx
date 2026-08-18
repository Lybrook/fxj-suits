import type { Metadata } from "next";
import "../src/index.css";

export const metadata: Metadata = {
  title: "FXJ Suits | Law Firm Operations",
  description: "A modern workspace for court cases, transactions, clients, and legal workflows.",
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
