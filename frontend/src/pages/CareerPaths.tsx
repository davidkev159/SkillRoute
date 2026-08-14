import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { api, ApiError } from "../api/client";
import { useApi } from "../lib/useApi";
import { Card, PageHeader, Pill } from "../components/ui";
import { EmptyState, ErrorState, LoadingState } from "../components/States";
import type { CareerPathResult } from "../api/types";

export default function CareerPaths() {
  const rolesState = useApi(api.listRoles, []);
  const [fromRoleId, setFromRoleId] = useState("");
  const [toRoleId, setToRoleId] = useState("");
  const [result, setResult] = useState<CareerPathResult | null>(null);
  const [running, setRunning] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function run() {
    if (!fromRoleId || !toRoleId || fromRoleId === toRoleId) return;
    setRunning(true);
    setError(null);
    try {
      setResult(await api.getCareerPath(fromRoleId, toRoleId));
    } catch (err) {
      setError(err instanceof ApiError ? err.message : "Something went wrong.");
      setResult(null);
    } finally {
      setRunning(false);
    }
  }

  useEffect(() => {
    if (fromRoleId && toRoleId && fromRoleId !== toRoleId) run();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [fromRoleId, toRoleId]);

  return (
    <div>
      <PageHeader
        title="Career Paths"
        description="See real precedent: people who actually held role A and later role B, and the skills they picked up along the way."
      />

      <Card className="p-5 mb-8">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <RoleSelect
            label="Starting role"
            value={fromRoleId}
            onChange={setFromRoleId}
            roles={rolesState.status === "success" ? rolesState.data : []}
          />
          <RoleSelect
            label="Target role"
            value={toRoleId}
            onChange={setToRoleId}
            roles={rolesState.status === "success" ? rolesState.data : []}
          />
        </div>
        {fromRoleId && fromRoleId === toRoleId && (
          <p className="mt-3 text-xs text-amber-400">Pick two different roles to compare.</p>
        )}
      </Card>

      {running && <LoadingState label="Searching career histories…" />}
      {error && <ErrorState message={error} onRetry={run} />}
      {!running && !error && !result && (
        <EmptyState title="No comparison yet" description="Pick a starting role and a target role above." />
      )}
      {!running && result && <CareerResults result={result} />}
    </div>
  );
}

function RoleSelect({
  label,
  value,
  onChange,
  roles,
}: {
  label: string;
  value: string;
  onChange: (v: string) => void;
  roles: { id: string; title: string }[];
}) {
  return (
    <div>
      <label className="text-xs font-medium text-ink-500 uppercase tracking-wide">{label}</label>
      <select
        value={value}
        onChange={(e) => onChange(e.target.value)}
        className="mt-2 w-full px-3 py-2 rounded-lg border border-ink-200 text-sm bg-ink-100 focus:outline-none focus:ring-2 focus:ring-accent-100 focus:border-accent-400"
      >
        <option value="">Select a role…</option>
        {roles.map((r) => (
          <option key={r.id} value={r.id}>
            {r.title}
          </option>
        ))}
      </select>
    </div>
  );
}

function CareerResults({ result }: { result: CareerPathResult }) {
  if (result.precedent_count === 0) {
    return (
      <EmptyState
        title="No precedent found in the graph"
        description={`Nobody in the seed data has held both ${result.from_role.title} and ${result.to_role.title} in that order — try a different pair.`}
      />
    );
  }

  return (
    <div className="space-y-8">
      <div className="px-4 py-3 rounded-lg bg-ink-100 border border-ink-200 inline-block">
        <p className="text-xs text-ink-400">People who made this move</p>
        <p className="text-lg font-semibold text-ink-900">{result.precedent_count}</p>
      </div>

      <div>
        <h2 className="mb-3 text-sm font-semibold text-ink-700 uppercase tracking-wide">
          Skills people commonly picked up
        </h2>
        {result.commonly_gained_skills.length === 0 ? (
          <EmptyState
            title="No clear skill pattern"
            description="People made this move without a common new skill showing up in the data."
          />
        ) : (
          <div className="flex flex-wrap gap-2">
            {result.commonly_gained_skills.map((s) => (
              <Link key={s.id} to={`/skills/${s.id}`}>
                <Pill>
                  {s.name} · {s.person_count}
                </Pill>
              </Link>
            ))}
          </div>
        )}
      </div>

      <div>
        <h2 className="mb-3 text-sm font-semibold text-ink-700 uppercase tracking-wide">
          Example people
        </h2>
        <div className="space-y-2">
          {result.examples.map((ex) => (
            <Card key={ex.person.id} className="p-4">
              <p className="text-sm font-medium text-ink-800">{ex.person.name}</p>
              <p className="text-xs text-ink-400">now {ex.person.current_role_title}</p>
              {ex.gained_skills.length > 0 && (
                <p className="mt-2 text-xs text-ink-500">
                  Picked up: {ex.gained_skills.map((s) => s.name).join(", ")}
                </p>
              )}
            </Card>
          ))}
        </div>
      </div>
    </div>
  );
}
