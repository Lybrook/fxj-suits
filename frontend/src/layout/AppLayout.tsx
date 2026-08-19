import Sidebar from "../components/Sidebar";

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
    <div className={`fxj-app-shell ${!isOnline ? "has-offline-banner" : ""} ${updateAvailable ? "has-update-banner" : ""}`}>
      <Sidebar />
      <main className="fxj-main-content">
        <div className="page-enter">{children}</div>
      </main>
    </div>
  );
}
