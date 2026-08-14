import { Link } from "react-router-dom";
import { api } from "../api/client";
import { useApi } from "../lib/useApi";
import { Card, CategoryTag, Pill, PageHeader } from "../components/ui";
import { EmptyState, ErrorState, LoadingState } from "../components/States";

export default function Bottlenecks() {
  const state = useApi(() => api.getBottlenecks(12), []);

  return (
    <div>
      <PageHeader
        title="Bottleneck Skills"
        description="For every role's required skills, we walk each one's prerequisite chain and count how many distinct roles it ultimately unlocks. High scorers are the highest-leverage skills to learn first."
      />

      {state.status === "loading" && <LoadingState label="Ranking skills…" />}
      {state.status === "error" && <ErrorState message={state.error} />}
      {state.status === "success" && state.data.length === 0 && (
        <EmptyState title="Nothing to rank yet" />
      )}

      {state.status === "success" && state.data.length > 0 && (
        <div className="space-y-3">
          {state.data.map((b, i) => {
            const maxCount = state.data[0].unlocked_role_count;
            const width = Math.max(8, (b.unlocked_role_count / maxCount) * 100);
            return (
              <Card key={b.skill.id} className="p-4">
                <div className="flex items-start justify-between gap-3 flex-wrap">
                  <div className="flex items-center gap-3">
                    <span className="text-sm font-medium text-ink-300 w-5 text-right">{i + 1}</span>
                    <div>
                      <Link
                        to={`/skills/${b.skill.id}`}
                        className="font-medium text-ink-900 hover:text-accent-400 transition-colors"
                      >
                        {b.skill.name}
                      </Link>
                      <div className="mt-1">
                        <CategoryTag category={b.skill.category} />
                      </div>
                    </div>
                  </div>
                  <p className="text-sm text-ink-500">
                    unlocks <span className="font-semibold text-ink-900">{b.unlocked_role_count}</span> role
                    {b.unlocked_role_count !== 1 ? "s" : ""}
                  </p>
                </div>
                <div className="mt-3 h-1.5 rounded-full bg-ink-50 overflow-hidden">
                  <div className="h-full bg-accent-500 rounded-full" style={{ width: `${width}%` }} />
                </div>
                <div className="mt-3 flex flex-wrap gap-1.5">
                  {b.unlocked_roles.slice(0, 8).map((role) => (
                    <Link key={role.id} to={`/roles/${role.id}`}>
                      <Pill>{role.title}</Pill>
                    </Link>
                  ))}
                  {b.unlocked_roles.length > 8 && (
                    <span className="text-xs text-ink-400 self-center">
                      +{b.unlocked_roles.length - 8} more
                    </span>
                  )}
                </div>
              </Card>
            );
          })}
        </div>
      )}
    </div>
  );
}
