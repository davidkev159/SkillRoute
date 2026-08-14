import { Link, useParams } from "react-router-dom";
import { api } from "../api/client";
import { useApi } from "../lib/useApi";
import { Card, ImportanceBadge, LevelBadge } from "../components/ui";
import { ErrorState, LoadingState } from "../components/States";

export default function RoleDetail() {
  const { roleId } = useParams<{ roleId: string }>();
  const state = useApi(() => api.getRole(roleId!), [roleId]);

  if (state.status === "loading") return <LoadingState label="Loading role…" />;
  if (state.status === "error") return <ErrorState message={state.error} />;

  const role = state.data;

  return (
    <div>
      <Link to="/roles" className="text-sm text-ink-400 hover:text-ink-600 transition-colors">
        ← All roles
      </Link>

      <div className="mt-3 flex items-start justify-between gap-4 flex-wrap">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-2xl font-display font-semibold tracking-tight text-ink-900">{role.title}</h1>
            <LevelBadge level={role.level} />
          </div>
          <p className="mt-2 text-sm text-ink-500 max-w-xl leading-relaxed">{role.description}</p>
          <p className="mt-2 text-xs text-ink-400">
            {role.people_count} {role.people_count === 1 ? "person has" : "people have"} held this role
          </p>
        </div>
        <Link
          to={`/gap-report?role=${role.id}`}
          className="px-4 py-2 rounded-lg bg-accent-600 text-white text-sm font-medium hover:bg-accent-500 transition-colors shrink-0"
        >
          Run a Gap Report for this role
        </Link>
      </div>

      <h2 className="mt-8 mb-3 text-sm font-semibold text-ink-700 uppercase tracking-wide">
        Required skills
      </h2>
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
        {role.requirements.map((req) => (
          <Card key={req.skill.id} className="p-4">
            <div className="flex items-center justify-between gap-2">
              <Link
                to={`/skills/${req.skill.id}`}
                className="font-medium text-ink-900 hover:text-accent-400 transition-colors"
              >
                {req.skill.name}
              </Link>
              <ImportanceBadge importance={req.importance} />
            </div>
            <p className="mt-1 text-xs text-ink-400">
              {req.skill.category} · min. level {req.min_level}/5
            </p>
          </Card>
        ))}
      </div>
    </div>
  );
}
