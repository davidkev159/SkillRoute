import { Link } from "react-router-dom";
import { Card } from "../components/ui";

const FEATURES = [
  {
    to: "/gap-report",
    title: "Gap Report",
    description: "Pick a target role and see exactly which skills you're missing — plus the shortest course path to close the gap.",
  },
  {
    to: "/bottlenecks",
    title: "Bottleneck Skills",
    description: "Which single skill, once learned, unlocks the most roles across the market?",
  },
  {
    to: "/career-paths",
    title: "Career Paths",
    description: "See real precedent: what skills did people actually pick up moving from one role to another?",
  },
  {
    to: "/roles",
    title: "Role & Skill Explorer",
    description: "Browse roles and skills, including full prerequisite chains and who teaches what.",
  },
];

export default function Home() {
  return (
    <div>
      <div className="max-w-2xl">
        <h1 className="text-3xl font-semibold tracking-tight text-ink-900">
          Find the shortest path to your next role.
        </h1>
        <p className="mt-3 text-ink-500 leading-relaxed">
          SkillRoute models careers as a graph: skills that require other skills, roles that
          require skills, and courses that teach them. That makes questions like{" "}
          <span className="text-ink-700">"what's missing, and what's the fastest way to close the gap?"</span>{" "}
          a natural traversal instead of a pile of joins.
        </p>
        <div className="mt-6 flex gap-3">
          <Link
            to="/gap-report"
            className="px-4 py-2 rounded-lg bg-accent-600 text-white text-sm font-medium hover:bg-accent-500 transition-colors"
          >
            Try a Gap Report
          </Link>
          <Link
            to="/roles"
            className="px-4 py-2 rounded-lg border border-ink-200 text-ink-700 text-sm font-medium hover:bg-ink-50 transition-colors"
          >
            Browse roles
          </Link>
        </div>
      </div>

      <div className="mt-12 grid grid-cols-1 sm:grid-cols-2 gap-4">
        {FEATURES.map((f) => (
          <Link key={f.to} to={f.to}>
            <Card className="p-5 h-full hover:border-accent-200 hover:shadow-none transition-colors">
              <p className="font-medium text-ink-900">{f.title}</p>
              <p className="mt-1.5 text-sm text-ink-500 leading-relaxed">{f.description}</p>
            </Card>
          </Link>
        ))}
      </div>
    </div>
  );
}
