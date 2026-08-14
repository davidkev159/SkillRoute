import { Link } from "react-router-dom";

export default function NotFound() {
  return (
    <div className="py-20 text-center">
      <p className="text-sm text-ink-400">404</p>
      <p className="mt-1 text-ink-700 font-medium">This page doesn't exist.</p>
      <Link to="/" className="mt-4 inline-block text-sm text-accent-400 hover:text-accent-500">
        Back home
      </Link>
    </div>
  );
}
