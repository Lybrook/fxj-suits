import { useEffect, useState } from "react";
import { Link, useLocation } from "react-router-dom";
import {
  Archive,
  BarChart3,
  BriefcaseBusiness,
  CalendarDays,
  ChevronLeft,
  ChevronRight,
  CircleDollarSign,
  ClipboardList,
  Cloud,
  FileCheck2,
  FileText,
  Gavel,
  LayoutDashboard,
  LogOut,
  Menu,
  PanelLeftClose,
  PanelLeftOpen,
  ReceiptText,
  Scale,
  ScrollText,
  Settings2,
  ShieldCheck,
  Users,
  X,
  type LucideIcon,
} from "lucide-react";
import { useAppContext } from "../context/AppContext";

interface MenuItem {
  label: string;
  path: string;
  icon: LucideIcon;
  show: boolean;
}

interface MenuSection {
  label: string;
  items: MenuItem[];
}

export default function Sidebar() {
  const { currentUser, logout, syncToCloud } = useAppContext();
  const location = useLocation();
  const [isOpen, setIsOpen] = useState(false);
  const [isSyncing, setIsSyncing] = useState(false);
  const [isCollapsed, setIsCollapsed] = useState(() => {
    if (typeof window === "undefined") return false;
    return window.localStorage.getItem("sidebarCollapsed") === "true";
  });

  useEffect(() => {
    window.localStorage.setItem("sidebarCollapsed", isCollapsed.toString());
  }, [isCollapsed]);

  useEffect(() => {
    setIsOpen(false);
  }, [location.pathname]);

  if (!currentUser) return null;

  const role = currentUser.role;
  const isAdmin = role === "admin";
  const isAccountant = role === "accountant";
  const isManager = role === "manager";
  const isManagingPartner = role === "managing_partner";
  const isStaff = isAdmin || isAccountant || isManager || isManagingPartner;
  const canManageMatters = isAdmin || isManager || isManagingPartner;
  const initials = currentUser.name
    ?.split(" ")
    .map((part) => part[0])
    .join("")
    .slice(0, 2)
    .toUpperCase() || "FX";

  const menuSections: MenuSection[] = [
    {
      label: "Workspace",
      items: [
        { label: "Dashboard", path: "/", icon: LayoutDashboard, show: isStaff },
        { label: "Court Calendar", path: "/court-calendar", icon: CalendarDays, show: isAdmin || isManager || isManagingPartner || isAccountant },
        { label: "Reports", path: "/reports", icon: BarChart3, show: isStaff },
        { label: "Performance", path: "/performance", icon: BarChart3, show: isAdmin },
      ],
    },
    {
      label: "Matters & filings",
      items: [
        { label: "Court Cases", path: "/court-cases", icon: Gavel, show: canManageMatters },
        { label: "Letters", path: "/letters", icon: FileText, show: canManageMatters },
        { label: "Land Titles", path: "/land-titles", icon: ScrollText, show: canManageMatters },
        { label: "Archive", path: "/archive", icon: Archive, show: canManageMatters },
        { label: "Requisitions", path: "/requisitions", icon: ClipboardList, show: true },
      ],
    },
    {
      label: "Clients & finance",
      items: [
        { label: "Clients", path: "/clients", icon: Users, show: isStaff },
        { label: "Transactions", path: "/transactions", icon: CircleDollarSign, show: canManageMatters },
        { label: "Invoices", path: "/invoices", icon: ReceiptText, show: isStaff },
        { label: "Expenses", path: "/expenses", icon: BriefcaseBusiness, show: isAccountant || isAdmin },
      ],
    },
    {
      label: "Administration",
      items: [
        { label: "Lawyers List", path: "/lawyers", icon: Scale, show: isAdmin },
        { label: "Add User / Staff", path: "/AddUser", icon: ShieldCheck, show: isAdmin },
      ],
    },
  ];

  const handleManualSync = async () => {
    if (isSyncing) return;
    setIsSyncing(true);
    try {
      await syncToCloud();
    } finally {
      window.setTimeout(() => setIsSyncing(false), 500);
    }
  };

  return (
    <>
      <button
        type="button"
        onClick={() => setIsOpen((open) => !open)}
        className="fxj-mobile-menu-button"
        aria-label={isOpen ? "Close navigation" : "Open navigation"}
        aria-expanded={isOpen}
      >
        {isOpen ? <X size={20} /> : <Menu size={20} />}
      </button>

      {isOpen && <button type="button" className="fxj-sidebar-backdrop" onClick={() => setIsOpen(false)} aria-label="Close navigation overlay" />}

      <aside className={`fxj-sidebar ${isOpen ? "is-open" : ""} ${isCollapsed ? "is-collapsed" : ""}`} aria-label="Main navigation">
        <div className="fxj-sidebar__topline" />
        <div className="fxj-sidebar__header">
          <Link to="/" className="fxj-sidebar__brand" aria-label="FXJ Suits dashboard">
            <span className="fxj-brand-mark" aria-hidden="true">FXJ</span>
            <span className="fxj-sidebar__brand-copy">
              <strong>FXJ Suits</strong>
              <small>Powered by Fikia × Jenga</small>
            </span>
          </Link>
          <button
            type="button"
            className="fxj-sidebar__collapse"
            onClick={() => setIsCollapsed((collapsed) => !collapsed)}
            aria-label={isCollapsed ? "Expand sidebar" : "Collapse sidebar"}
            title={isCollapsed ? "Expand sidebar" : "Collapse sidebar"}
          >
            {isCollapsed ? <PanelLeftOpen size={17} /> : <PanelLeftClose size={17} />}
          </button>
        </div>

        <div className="fxj-sidebar__user">
          <span className="fxj-sidebar__avatar" aria-hidden="true">{initials}</span>
          <span className="fxj-sidebar__user-copy">
            <strong>{currentUser.name || "Workspace user"}</strong>
            <small>{role.replace("_", " ")}</small>
          </span>
          <Settings2 className="fxj-sidebar__user-icon" size={15} aria-hidden="true" />
        </div>

        <nav className="fxj-sidebar__nav">
          {menuSections.map((section) => {
            const visibleItems = section.items.filter((item) => item.show);
            if (visibleItems.length === 0) return null;
            return (
              <div className="fxj-sidebar__section" key={section.label}>
                <p className="fxj-sidebar__section-label">{section.label}</p>
                {visibleItems.map((item) => {
                  const Icon = item.icon;
                  const isActive = item.path === "/" ? location.pathname === "/" : location.pathname.startsWith(item.path);
                  return (
                    <Link
                      key={item.path}
                      to={item.path}
                      className={`fxj-sidebar__link ${isActive ? "is-active" : ""}`}
                      title={isCollapsed ? item.label : undefined}
                      aria-current={isActive ? "page" : undefined}
                    >
                      <Icon size={17} strokeWidth={isActive ? 2.2 : 1.8} aria-hidden="true" />
                      <span>{item.label}</span>
                      {isActive && <span className="fxj-sidebar__active-marker" aria-hidden="true" />}
                    </Link>
                  );
                })}
              </div>
            );
          })}
        </nav>

        <div className="fxj-sidebar__footer">
          <button type="button" className="fxj-sidebar__utility" onClick={handleManualSync} disabled={isSyncing}>
            <Cloud size={17} className={isSyncing ? "fxj-spin" : ""} aria-hidden="true" />
            <span>{isSyncing ? "Syncing workspace…" : "Sync workspace"}</span>
          </button>
          <button type="button" className="fxj-sidebar__logout" onClick={logout}>
            <LogOut size={17} aria-hidden="true" />
            <span>Sign out</span>
          </button>
          <p className="fxj-sidebar__version">FXJ SUITS · KENYA · V1.10.0</p>
        </div>
      </aside>
    </>
  );
}
