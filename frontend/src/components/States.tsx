import type { ReactNode } from "react";

export function LoadingState({ label = "Loading…" }: { label?: string }) {
  return (
    <div className="flex items-center gap-3 py-16 justify-center text-ink-400">
      <span className="h-4 w-4 rounded-full border-2 border-ink-200 border-t-accent-500 animate-spin" />
      <span className="text-sm">{label}</span>
    </div>
  );
}

export function ErrorState({ message, onRetry }: { message: string; onRetry?: () => void }) {
  return (
    <div className="flex flex-col items-center gap-3 py-16 text-center px-6">
      <div className="h-10 w-10 rounded-full bg-red-50 text-red-500 flex items-center justify-center text-lg">
        !
      </div>
      <p className="text-sm text-ink-600 max-w-sm">{message}</p>
      {onRetry && (
        <button
          onClick={onRetry}
          className="mt-1 text-sm font-medium text-accent-600 hover:text-accent-500 transition-colors"
        >
          Try again
        </button>
      )}
    </div>
  );
}

export function EmptyState({ title, description, icon }: { title: string; description?: string; icon?: ReactNode }) {
  return (
    <div className="flex flex-col items-center gap-2 py-16 text-center px-6">
      {icon && <div className="text-ink-300 text-2xl mb-1">{icon}</div>}
      <p className="text-sm font-medium text-ink-700">{title}</p>
      {description && <p className="text-sm text-ink-400 max-w-sm">{description}</p>}
    </div>
  );
}
