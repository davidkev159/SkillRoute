import { useMemo, useState } from "react";
import { Link } from "react-router-dom";
import { api } from "../api/client";
import { useApi } from "../lib/useApi";
import { Card, LevelBadge, PageHeader } from "../components/ui";
import { EmptyState, ErrorState, LoadingState } from "../components/States";

export default function RolesList() {
  const state = useApi(api.listRoles, []);
  const [query, setQuery] = useState("");

  const filtered = useMemo(() => {
    if (state.status !== "success") return [];
    const q = query.trim().toLowerCase();
    if (!q) return state.data;
    return state.data.filter((r) => r.title.toLowerCase().includes(q));
  }, [state, query]);

  return (
    <div>
      <PageHeader
        title="Roles"
        description="Every role's skill requirements live in the graph — click one to see what it takes."
      />

      <input
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Search roles…"
        className="w-full max-w-sm px-3 py-2 rounded-lg border border-ink-200 text-sm placeholder:text-ink-300 focus:outline-none focus:ring-2 focus:ring-accent-100 focus:border-accent-400 transition-colors mb-6"
      />

      {state.status === "loading" && <LoadingState label="Loading roles…" />}
      {state.status === "error" && <ErrorState message={state.error} />}
      {state.status === "success" && filtered.length === 0 && (
        <EmptyState title="No roles match your search" description="Try a different keyword." />
      )}
      {state.status === "success" && filtered.length > 0 && (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {filtered.map((role) => (
            <Link key={role.id} to={`/roles/${role.id}`}>
              <Card className="p-5 h-full hover:border-accent-200 hover:shadow-none transition-colors">
                <div className="flex items-start justify-between gap-2">
                  <p className="font-medium text-ink-900">{role.title}</p>
                  <LevelBadge level={role.level} />
                </div>
                <p className="mt-2 text-sm text-ink-500 leading-relaxed line-clamp-3">{role.description}</p>
              </Card>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}
