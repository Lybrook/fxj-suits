#!/usr/bin/env python3
content = '''import Sidebar from "../components/Sidebar";

/* =============================================
   FXJ SUITS — App Layout
   Wraps all authenticated pages with the sidebar
============================================= */

export default function AppLayout({
  children,
  isOnline = true,
  updateAvailable = false,
}: {
  children: React.ReactNode;
  isOnline?: boolean;
  updateAvailable?: boolean;
}) {
  return (
    <div className="flex" style={{ backgroundColor: "var(--fxj-light)", minHeight: "100vh" }}>
      <Sidebar />
      <main
        className="flex-1 min-h-screen"
        style={{
          marginLeft: 240,
          padding: "24px",
          paddingTop: (isOnline ? 0 : 40) + (updateAvailable ? 74 : 0) + 24,
          backgroundColor: "var(--fxj-light)",
          transition: "margin-left 0.3s ease",
        }}
      >
        <div className="page-enter">{children}</div>
      </main>
    </div>
  );
}
'''

with open("/home/ubuntu/fxj-suits/src/layout/AppLayout.tsx", "w", encoding="utf-8") as f:
    f.write(content)
print("AppLayout.tsx written successfully")
