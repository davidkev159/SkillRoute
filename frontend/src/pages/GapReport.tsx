import { useEffect, useMemo, useState } from "react";
import { Link, useSearchParams } from "react-router-dom";
import { api } from "../api/client";
import { useApi } from "../lib/useApi";
import { Card, ImportanceBadge, PageHeader } from "../components/ui";
import { EmptyState, ErrorState, LoadingState } from "../components/States";
import { ApiError } from "../api/client";
import type { GapAnalysisResult } from "../api/types";

type Mode = "persona" | "manual";

export default function GapReport() {
  const [searchParams] = useSearchParams();
  const peopleState = useApi(api.listPeople, []);
  const rolesState = useApi(api.listRoles, []);

  const [mode, setMode] = useState<Mode>("persona");
  const [personId, setPersonId] = useState<string>("");
  const [manualSkillIds, setManualSkillIds] = useState<string[]>([]);
  const [roleId, setRoleId] = useState<string>(searchParams.get("role") ?? "");

  const personState = useApi(
    () => (personId ? api.getPerson(personId) : Promise.resolve(null)),
    [personId],
  );

  const skillsState = useApi(api.listSkills, []);

  const knownSkillIds = useMemo(() => {
    if (mode === "manual") return manualSkillIds;
    if (personState.status === "success" && personState.data) {
      return personState.data.skills.map((s) => s.skill.id);
    }
    return [];
  }, [mode, manualSkillIds, personState]);

  const [result, setResult] = useState<GapAnalysisResult | null>(null);
  const [running, setRunning] = useState(false);
  const [runError, setRunError] = useState<string | null>(null);

  async function runAnalysis() {
    if (!roleId) return;
    setRunning(true);
    setRunError(null);
    try {
      const data = await api.getGapAnalysis(roleId, knownSkillIds);
      setResult(data);
    } catch (err) {
      setRunError(err instanceof ApiError ? err.message : "Something went wrong.");
      setResult(null);
    } finally {
      setRunning(false);
    }
  }

  // Auto-run once we have a role and (for persona mode) the profile has loaded.
  useEffect(() => {
    if (!roleId) return;
    if (mode === "persona" && !personId) return;
    if (mode === "persona" && personState.status === "loading") return;
    runAnalysis();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [roleId, mode, personId, personState.status]);

  return (
    <div>
      <PageHeader
        title="Gap Report"
        description="Pick who you are (or hand-pick skills) and where you want to go — SkillRoute finds what's missing and the shortest course path to close it."
      />

      <Card className="p-5 mb-8">
        <div className="flex items-center gap-2 mb-4">
          <ModeButton active={mode === "persona"} onClick={() => setMode("persona")}>
            Pick a persona
          </ModeButton>
          <ModeButton active={mode === "manual"} onClick={() => setMode("manual")}>
            Pick skills manually
          </ModeButton>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label className="text-xs font-medium text-ink-500 uppercase tracking-wide">
              {mode === "persona" ? "I am…" : "Skills I already have"}
            </label>
            {mode === "persona" ? (
              peopleState.status === "loading" ? (
                <LoadingState label="Loading people…" />
              ) : peopleState.status === "error" ? (
                <ErrorState message={peopleState.error} />
              ) : (
                <select
                  value={personId}
                  onChange={(e) => setPersonId(e.target.value)}
                  className="mt-2 w-full px-3 py-2 rounded-lg border border-ink-200 text-sm bg-white focus:outline-none focus:ring-2 focus:ring-accent-100 focus:border-accent-400"
                >
                  <option value="">Select a person…</option>
                  {peopleState.data.map((p) => (
                    <option key={p.id} value={p.id}>
                      {p.name} — {p.current_role_title}
                    </option>
                  ))}
                </select>
              )
            ) : skillsState.status === "success" ? (
              <div className="mt-2 max-h-48 overflow-y-auto border border-ink-100 rounded-lg p-3 flex flex-wrap gap-1.5">
                {skillsState.data.map((s) => {
                  const active = manualSkillIds.includes(s.id);
                  return (
                    <button
                      key={s.id}
                      onClick={() =>
                        setManualSkillIds((prev) =>
                          active ? prev.filter((id) => id !== s.id) : [...prev, s.id],
                        )
                      }
                      className={`px-2.5 py-1 rounded-md text-xs font-medium transition-colors ${
                        active ? "bg-accent-600 text-white" : "bg-ink-50 text-ink-600 hover:bg-ink-100"
                      }`}
                    >
                      {s.name}
                    </button>
                  );
                })}
              </div>
            ) : (
              <LoadingState label="Loading skills…" />
            )}
          </div>

          <div>
            <label className="text-xs font-medium text-ink-500 uppercase tracking-wide">
              Target role
            </label>
            {rolesState.status === "success" ? (
              <select
                value={roleId}
                onChange={(e) => setRoleId(e.target.value)}
                className="mt-2 w-full px-3 py-2 rounded-lg border border-ink-200 text-sm bg-white focus:outline-none focus:ring-2 focus:ring-accent-100 focus:border-accent-400"
              >
                <option value="">Select a role…</option>
                {rolesState.data.map((r) => (
                  <option key={r.id} value={r.id}>
                    {r.title}
                  </option>
                ))}
              </select>
            ) : (
              <LoadingState label="Loading roles…" />
            )}

            {mode === "manual" && (
              <button
                onClick={runAnalysis}
                disabled={!roleId || running}
                className="mt-4 w-full px-4 py-2 rounded-lg bg-accent-600 text-white text-sm font-medium hover:bg-accent-500 disabled:opacity-40 disabled:cursor-not-allowed transition-colors"
              >
                {running ? "Analyzing…" : "Analyze gap"}
              </button>
            )}
          </div>
        </div>
      </Card>

      {running && <LoadingState label="Analyzing the graph…" />}
      {runError && <ErrorState message={runError} onRetry={runAnalysis} />}

      {!running && !runError && !result && (
        <EmptyState
          title="No report yet"
          description="Choose who you are and a target role above to see your skill gap."
        />
      )}

      {!running && result && <GapResults result={result} />}
    </div>
  );
}

function ModeButton({ active, onClick, children }: { active: boolean; onClick: () => void; children: React.ReactNode }) {
  return (
    <button
      onClick={onClick}
      className={`px-3 py-1.5 rounded-md text-sm font-medium transition-colors ${
        active ? "bg-ink-900 text-white" : "bg-ink-50 text-ink-500 hover:bg-ink-100"
      }`}
    >
      {children}
    </button>
  );
}

function GapResults({ result }: { result: GapAnalysisResult }) {
  if (result.missing.length === 0) {
    return (
      <EmptyState
        title={`No gap — fully ready for ${result.role.title}`}
        description="Every required skill is already covered."
      />
    );
  }

  return (
    <div className="space-y-8">
      <div className="flex flex-wrap items-center gap-4">
        <Stat label="Missing skills" value={String(result.missing.length)} />
        <Stat label="Already have" value={String(result.already_has.length)} />
        <Stat label="Recommended path" value={`${result.recommended_path_hours}h`} />
      </div>

      <div>
        <h2 className="mb-3 text-sm font-semibold text-ink-700 uppercase tracking-wide">
          Missing skills for {result.role.title}
        </h2>
        <div className="space-y-3">
          {result.missing.map((m) => (
            <Card key={m.skill.id} className="p-4">
              <div className="flex items-start justify-between gap-2 flex-wrap">
                <div>
                  <Link
                    to={`/skills/${m.skill.id}`}
                    className="font-medium text-ink-900 hover:text-accent-600 transition-colors"
                  >
                    {m.skill.name}
                  </Link>
                  <p className="text-xs text-ink-400">{m.skill.category} · min. level {m.min_level}/5</p>
                </div>
                <ImportanceBadge importance={m.importance} />
              </div>
              {m.prerequisite_chain.length > 0 && (
                <p className="mt-2 text-xs text-ink-400">
                  First learn: {m.prerequisite_chain.map((s) => s.name).join(" → ")}
                </p>
              )}
              {m.covering_courses.length > 0 && (
                <p className="mt-1 text-xs text-ink-500">
                  Covered by: {m.covering_courses.map((c) => c.title).join(", ")}
                </p>
              )}
            </Card>
          ))}
        </div>
      </div>

      <div>
        <h2 className="mb-3 text-sm font-semibold text-ink-700 uppercase tracking-wide">
          Recommended learning path ({result.recommended_path_hours}h total)
        </h2>
        <ol className="space-y-2">
          {result.recommended_courses.map((c, i) => (
            <li key={c.id} className="flex items-center gap-3">
              <span className="h-6 w-6 shrink-0 rounded-full bg-ink-100 text-ink-500 text-xs font-medium flex items-center justify-center">
                {i + 1}
              </span>
              <Card className="p-3 flex-1 flex items-center justify-between gap-3">
                <div>
                  <p className="text-sm font-medium text-ink-800">{c.title}</p>
                  <p className="text-xs text-ink-400">{c.provider} · {c.level}</p>
                </div>
                <span className="text-xs text-ink-400 shrink-0">{c.duration_hours}h</span>
              </Card>
            </li>
          ))}
        </ol>
      </div>
    </div>
  );
}

function Stat({ label, value }: { label: string; value: string }) {
  return (
    <div className="px-4 py-3 rounded-lg bg-white border border-ink-100">
      <p className="text-xs text-ink-400">{label}</p>
      <p className="text-lg font-semibold text-ink-900">{value}</p>
    </div>
  );
}
