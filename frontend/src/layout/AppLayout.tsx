import { Bell, ChevronRight, Command, Plus, Search, ShieldCheck } from "lucide-react";
import { Link, useLocation } from "react-router-dom";
import Sidebar from "../components/Sidebar";

const pageNames: Record<string, string> = {
  "/": "Overview",
  "/clients": "Clients",
  "/cases": "Matters",
  "/letters": "Correspondence",
  "/transactions": "Transactions",
  "/invoices": "Invoices",
  "/expenses": "Expenses",
  "/court-calendar": "Court calendar",
  "/performance": "Performance",
  "/reports": "Reports",
  "/requisitions": "Requisitions",
};

function currentPage(pathname: string) {
  const match = Object.entries(pageNames).find(([path]) => path !== "/" && pathname.startsWith(path));
  return match?.[1] ?? pageNames[pathname] ?? "Workspace";
}

export default function AppLayout({
  children,
  isOnline = true,
  updateAvailable = false,
}: {
  children: React.ReactNode;
  isOnline?: boolean;
  updateAvailable?: boolean;
}) {
  const location = useLocation();
  const page = currentPage(location.pathname);

  return (
    <div className={`fxj-app-shell ${!isOnline ? "has-offline-banner" : ""} ${updateAvailable ? "has-update-banner" : ""}`}>
      <Sidebar />
      <main className="fxj-main-content">
        <header className="fxj-context-bar" aria-label="Workspace context">
          <div className="fxj-context-bar__crumbs">
            <span className="fxj-context-bar__workspace">FXJ Suits</span>
            <ChevronRight size={14} aria-hidden="true" />
            <strong>{page}</strong>
          </div>
          <div className="fxj-context-bar__actions">
            <div className="fxj-command-search" aria-label="Search workspace">
              <Search size={15} aria-hidden="true" />
              <span>Search workspace</span>
              <kbd><Command size={11} aria-hidden="true" /> K</kbd>
            </div>
            <span className={`fxj-status-pill ${isOnline ? "is-online" : "is-offline"}`}>
              <span className="fxj-status-pill__dot" aria-hidden="true" />
              {isOnline ? "Synced" : "Offline"}
            </span>
            <span className="fxj-context-icon" title="Notifications" aria-label="Notifications"><Bell size={17} /></span>
            <Link className="fxj-new-matter" to="/requisitions"><Plus size={15} /> New request</Link>
            <span className="fxj-security-mark" title="Firm workspace protected" aria-label="Firm workspace protected"><ShieldCheck size={16} /></span>
          </div>
        </header>
        <div className="page-enter">{children}</div>
      </main>
    </div>
  );
}
