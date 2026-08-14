import type { ReactNode } from "react";

export function Card({ children, className = "" }: { children: ReactNode; className?: string }) {
  return (
    <div className={`bg-white border border-ink-100 rounded-xl shadow-card ${className}`}>{children}</div>
  );
}

export function PageHeader({ title, description }: { title: string; description?: string }) {
  return (
    <div className="mb-8">
      <h1 className="text-2xl font-semibold tracking-tight text-ink-900">{title}</h1>
      {description && <p className="mt-1.5 text-sm text-ink-500 max-w-2xl">{description}</p>}
    </div>
  );
}

const IMPORTANCE_STYLES: Record<string, string> = {
  core: "bg-accent-50 text-accent-600",
  important: "bg-amber-50 text-amber-600",
  "nice-to-have": "bg-ink-100 text-ink-500",
};

export function ImportanceBadge({ importance }: { importance: string }) {
  return (
    <span
      className={`inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium ${
        IMPORTANCE_STYLES[importance] ?? IMPORTANCE_STYLES["nice-to-have"]
      }`}
    >
      {importance}
    </span>
  );
}

export function CategoryTag({ category }: { category: string }) {
  return (
    <span className="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-ink-100 text-ink-500">
      {category}
    </span>
  );
}

export function LevelDots({ level, max = 5 }: { level: number; max?: number }) {
  return (
    <span className="inline-flex items-center gap-0.5" title={`Level ${level} of ${max}`}>
      {Array.from({ length: max }).map((_, i) => (
        <span
          key={i}
          className={`h-1.5 w-1.5 rounded-full ${i < level ? "bg-accent-500" : "bg-ink-100"}`}
        />
      ))}
    </span>
  );
}

export function LevelBadge({ level }: { level: string }) {
  return (
    <span className="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-ink-100 text-ink-600">
      {level}
    </span>
  );
}

export function Pill({ children }: { children: ReactNode }) {
  return (
    <span className="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-ink-100 text-ink-600 hover:bg-ink-200 transition-colors">
      {children}
    </span>
  );
}
