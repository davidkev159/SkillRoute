/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      fontFamily: {
        sans: ["Inter", "ui-sans-serif", "system-ui", "-apple-system", "sans-serif"],
        display: ["Cal Sans", "Inter", "ui-sans-serif", "system-ui", "sans-serif"],
      },
      colors: {
        // Dark-first scale: 50 = page background (near-black), 900 = primary
        // text (near-white). Kept the same token names as the old light
        // theme so every existing `text-ink-900` / `bg-ink-50` usage across
        // the app just inherits the new dark values instead of needing a
        // rewrite.
        ink: {
          50: "#09090b",
          100: "#18181b",
          200: "#27272a",
          300: "#3f3f46",
          400: "#71717a",
          500: "#a1a1aa",
          600: "#d4d4d8",
          700: "#e4e4e7",
          800: "#f4f4f5",
          900: "#ffffff",
          950: "#ffffff",
        },
        accent: {
          50: "#14103a",
          100: "#211a5c",
          200: "#3c2fa3",
          400: "#9b85f8",
          500: "#7a5ff5",
          600: "#593bed",
        },
      },
      boxShadow: {
        card: "0 1px 0 0 rgb(255 255 255 / 0.04) inset, 0 10px 30px -14px rgb(0 0 0 / 0.7)",
      },
    },
  },
  plugins: [],
};
