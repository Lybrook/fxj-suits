import type { Metadata } from "next";
import "../src/index.css";

export const metadata: Metadata = {
  title: "FXJ Suits | Kenyan Legal Operations",
  description: "A calm, connected workspace for Kenyan legal teams, powered by Fikia × Jenga Tech.",
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en-KE">
      <body>{children}</body>
    </html>
  );
}
