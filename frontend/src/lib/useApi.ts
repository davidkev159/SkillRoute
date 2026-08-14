import { useEffect, useState } from "react";
import { ApiError } from "../api/client";

type AsyncState<T> =
  | { status: "loading" }
  | { status: "error"; error: string }
  | { status: "success"; data: T };

/** Runs `fetcher` whenever `deps` change, exposing a discriminated-union
 * status so pages render an explicit loading/error/success state instead of
 * flashing stale or undefined data. */
export function useApi<T>(fetcher: () => Promise<T>, deps: unknown[]): AsyncState<T> {
  const [state, setState] = useState<AsyncState<T>>({ status: "loading" });

  useEffect(() => {
    let cancelled = false;
    setState({ status: "loading" });
    fetcher()
      .then((data) => {
        if (!cancelled) setState({ status: "success", data });
      })
      .catch((err) => {
        if (cancelled) return;
        const message = err instanceof ApiError ? err.message : "Something went wrong.";
        setState({ status: "error", error: message });
      });
    return () => {
      cancelled = true;
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, deps);

  return state;
}
