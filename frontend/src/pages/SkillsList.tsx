import { useMemo, useState } from "react";
import { Link } from "react-router-dom";
import { api } from "../api/client";
import { useApi } from "../lib/useApi";
import { CategoryTag, PageHeader } from "../components/ui";
import { EmptyState, ErrorState, LoadingState } from "../components/States";

export default function SkillsList() {
  const state = useApi(api.listSkills, []);
  const [query, setQuery] = useState("");

  const grouped = useMemo(() => {
    if (state.status !== "success") return [];
    const q = query.trim().toLowerCase();
    const filtered = q ? state.data.filter((s) => s.name.toLowerCase().includes(q)) : state.data;
    const byCategory = new Map<string, typeof filtered>();
    for (const skill of filtered) {
      const list = byCategory.get(skill.category) ?? [];
      list.push(skill);
      byCategory.set(skill.category, list);
    }
    return Array.from(byCategory.entries());
  }, [state, query]);

  return (
    <div>
      <PageHeader
        title="Skills"
        description="Skills form a prerequisite graph — some skills depend on others being learned first."
      />

      <input
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Search skills…"
        className="w-full max-w-sm px-3 py-2 rounded-lg border border-ink-200 text-sm placeholder:text-ink-300 focus:outline-none focus:ring-2 focus:ring-accent-100 focus:border-accent-400 transition-colors mb-6"
      />

      {state.status === "loading" && <LoadingState label="Loading skills…" />}
      {state.status === "error" && <ErrorState message={state.error} />}
      {state.status === "success" && grouped.length === 0 && (
        <EmptyState title="No skills match your search" />
      )}

      <div className="space-y-8">
        {grouped.map(([category, skills]) => (
          <div key={category}>
            <h2 className="mb-3 text-sm font-semibold text-ink-700 uppercase tracking-wide">{category}</h2>
            <div className="flex flex-wrap gap-2">
              {skills.map((skill) => (
                <Link
                  key={skill.id}
                  to={`/skills/${skill.id}`}
                  className="px-3 py-1.5 rounded-lg border border-ink-100 bg-white text-sm text-ink-700 hover:border-accent-200 hover:text-accent-600 transition-colors"
                >
                  {skill.name}
                </Link>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
