/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        paper: "#F7F6F2",
        ink: "#1C1F26",
        ledger: "#2A2E37",
        burgundy: {
          DEFAULT: "#7A2331",
          dark: "#5C1A25",
          light: "#9C3B4A",
        },
        brass: {
          DEFAULT: "#A98942",
          light: "#C7A863",
        },
        parchment: "#EFEBDD",
        line: "#DEDACB",
      },
      fontFamily: {
        serif: ["'Source Serif 4'", "Georgia", "serif"],
        sans: ["'IBM Plex Sans'", "system-ui", "sans-serif"],
        mono: ["'IBM Plex Mono'", "monospace"],
      },
      boxShadow: {
        tab: "0 2px 0 0 rgba(0,0,0,0.04)",
      },
    },
  },
  plugins: [],
};
