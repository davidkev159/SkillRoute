import { NavLink, Outlet } from "react-router-dom";

const NAV_ITEMS = [
  { to: "/roles", label: "Roles" },
  { to: "/skills", label: "Skills" },
  { to: "/gap-report", label: "Gap Report" },
  { to: "/bottlenecks", label: "Bottleneck Skills" },
  { to: "/career-paths", label: "Career Paths" },
];

export default function Layout() {
  return (
    <div className="min-h-screen flex flex-col">
      <header className="border-b border-ink-200 bg-ink-50/75 backdrop-blur sticky top-0 z-10">
        <div className="max-w-6xl mx-auto px-6 h-16 flex items-center justify-between">
          <NavLink to="/" className="flex items-center gap-2 shrink-0">
            <span className="h-6 w-6 rounded-md bg-accent-600 flex items-center justify-center shadow-[0_0_16px_rgb(89_59_237_/_0.55)]">
              <span className="h-2 w-2 rounded-full bg-white" />
            </span>
            <span className="font-display font-semibold tracking-tight text-ink-900">SkillRoute</span>
          </NavLink>
          <nav className="flex items-center gap-1">
            {NAV_ITEMS.map((item) => (
              <NavLink
                key={item.to}
                to={item.to}
                className={({ isActive }) =>
                  `px-3 py-2 rounded-full text-sm font-medium transition-colors ${
                    isActive ? "bg-accent-100 text-accent-400" : "text-ink-400 hover:text-ink-900 hover:bg-ink-100"
                  }`
                }
              >
                {item.label}
              </NavLink>
            ))}
          </nav>
        </div>
      </header>
      <main className="flex-1 w-full">
        <div className="max-w-6xl mx-auto px-6 py-10">
          <Outlet />
        </div>
      </main>
      <footer className="border-t border-ink-200 py-6">
        <div className="max-w-6xl mx-auto px-6 text-xs text-ink-400">
          SkillRoute — a graph-powered career &amp; skill readiness demo, built on CognoDB.
        </div>
      </footer>
    </div>
  );
}
