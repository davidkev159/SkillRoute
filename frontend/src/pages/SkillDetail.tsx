import { Link, useParams } from "react-router-dom";
import { api } from "../api/client";
import { useApi } from "../lib/useApi";
import { Card, CategoryTag, LevelBadge } from "../components/ui";
import { EmptyState, ErrorState, LoadingState } from "../components/States";

export default function SkillDetail() {
  const { skillId } = useParams<{ skillId: string }>();
  const state = useApi(() => api.getSkill(skillId!), [skillId]);

  if (state.status === "loading") return <LoadingState label="Loading skill…" />;
  if (state.status === "error") return <ErrorState message={state.error} />;

  const skill = state.data;

  // Group the prerequisite chain by depth so it reads as a staircase:
  // depth 1 = learn this right before `skill`, higher depth = further back.
  const byDepth = new Map<number, typeof skill.prerequisites>();
  for (const p of skill.prerequisites) {
    const list = byDepth.get(p.depth) ?? [];
    list.push(p);
    byDepth.set(p.depth, list);
  }
  const depths = Array.from(byDepth.keys()).sort((a, b) => a - b);

  return (
    <div>
      <Link to="/skills" className="text-sm text-ink-400 hover:text-ink-600 transition-colors">
        ← All skills
      </Link>

      <div className="mt-3 flex items-center gap-2">
        <h1 className="text-2xl font-semibold tracking-tight text-ink-900">{skill.name}</h1>
        <CategoryTag category={skill.category} />
      </div>

      <div className="mt-8 grid grid-cols-1 lg:grid-cols-2 gap-8">
        <div>
          <h2 className="mb-3 text-sm font-semibold text-ink-700 uppercase tracking-wide">
            Prerequisite chain
          </h2>
          {depths.length === 0 ? (
            <EmptyState title="No prerequisites" description="This is a foundational skill." />
          ) : (
            <ol className="relative border-l border-ink-100 pl-5 space-y-4">
              {depths.map((depth) => (
                <li key={depth}>
                  <span className="absolute -left-[5px] mt-1.5 h-2.5 w-2.5 rounded-full bg-accent-400" />
                  <p className="text-xs text-ink-400 mb-1">{depth} hop{depth > 1 ? "s" : ""} away</p>
                  <div className="flex flex-wrap gap-2">
                    {byDepth.get(depth)!.map((p) => (
                      <Link
                        key={p.id}
                        to={`/skills/${p.id}`}
                        className="px-2.5 py-1 rounded-md border border-ink-100 bg-white text-sm text-ink-700 hover:border-accent-200 hover:text-accent-600 transition-colors"
                      >
                        {p.name}
                      </Link>
                    ))}
                  </div>
                </li>
              ))}
            </ol>
          )}
        </div>

        <div>
          <h2 className="mb-3 text-sm font-semibold text-ink-700 uppercase tracking-wide">
            Required by roles
          </h2>
          {skill.required_by_roles.length === 0 ? (
            <EmptyState title="No roles require this skill directly" />
          ) : (
            <div className="flex flex-wrap gap-2 mb-8">
              {skill.required_by_roles.map((role) => (
                <Link key={role.id} to={`/roles/${role.id}`}>
                  <Card className="px-3 py-1.5 flex items-center gap-2 hover:border-accent-200 hover:shadow-none transition-colors">
                    <span className="text-sm text-ink-700">{role.title}</span>
                    <LevelBadge level={role.level} />
                  </Card>
                </Link>
              ))}
            </div>
          )}

          <h2 className="mb-3 text-sm font-semibold text-ink-700 uppercase tracking-wide">
            Taught by courses
          </h2>
          {skill.taught_by_courses.length === 0 ? (
            <EmptyState title="No courses teach this skill yet" />
          ) : (
            <div className="space-y-2">
              {skill.taught_by_courses.map((course) => (
                <Card key={course.id} className="p-3 flex items-center justify-between gap-3">
                  <div>
                    <p className="text-sm font-medium text-ink-800">{course.title}</p>
                    <p className="text-xs text-ink-400">{course.provider} · {course.duration_hours}h · {course.level}</p>
                  </div>
                </Card>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
