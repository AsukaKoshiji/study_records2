import Link from "next/link";

const navItems = [
  { href: "/", label: "概要" },
  { href: "/records", label: "学習記録" },
  { href: "/goals", label: "目標登録" },
  { href: "/progress", label: "進捗" },
  { href: "/calendar", label: "カレンダー" }
];

export function AppShell({ children }: { children: React.ReactNode }) {
  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-mark">LR</div>
          <div>
            <p className="brand-title">Learning Record</p>
            <p className="brand-subtitle">Study management</p>
          </div>
        </div>
        <nav className="nav-list" aria-label="メインナビゲーション">
          {navItems.map((item) => (
            <Link href={item.href} key={item.href} className="nav-link">
              {item.label}
            </Link>
          ))}
        </nav>
      </aside>
      <main className="main-panel">{children}</main>
    </div>
  );
}
