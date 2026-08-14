/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      fontFamily: {
        sans: ["Inter", "ui-sans-serif", "system-ui", "-apple-system", "sans-serif"],
      },
      colors: {
        ink: {
          950: "#0b0d12",
          900: "#12151c",
          800: "#1b1f29",
          700: "#272c38",
          600: "#3a4152",
          500: "#565f74",
          400: "#7c8496",
          300: "#a7adba",
          200: "#d3d6dd",
          100: "#eaecef",
          50: "#f6f7f8",
        },
        accent: {
          600: "#4f46e5",
          500: "#6366f1",
          400: "#818cf8",
          100: "#e0e7ff",
          50: "#eef0ff",
        },
      },
      boxShadow: {
        card: "0 1px 2px 0 rgb(0 0 0 / 0.04), 0 1px 6px -2px rgb(0 0 0 / 0.06)",
      },
    },
  },
  plugins: [],
};
