import type { Config } from "tailwindcss";
import animate from "tailwindcss-animate";

const config: Config = {
  darkMode: "class",
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        // ----------------------------------------------------------------
        // Brand / accent
        // ----------------------------------------------------------------
        accent: {
          DEFAULT: "#4F46E5", // indigo-600
          foreground: "#FFFFFF",
        },

        // ----------------------------------------------------------------
        // Surface colours
        // ----------------------------------------------------------------
        background: {
          DEFAULT: "#FAFAFA", // near-white
          dark: "#0A0A0A",   // near-black
        },
        foreground: {
          DEFAULT: "#0F172A", // slate-900
          dark: "#F8FAFC",   // slate-50
        },

        // ----------------------------------------------------------------
        // Gray scale anchors
        // ----------------------------------------------------------------
        surface: {
          50: "#F9FAFB",   // gray-50
          100: "#F3F4F6",
          200: "#E5E7EB",
          800: "#1F2937",
          900: "#111827",
          950: "#030712",  // near gray-950
        },

        // ----------------------------------------------------------------
        // Evidence-tier semantic colours
        // ----------------------------------------------------------------
        evidence: {
          self: "#6B7280",     // gray-500 — self_reported
          ai: "#D97706",       // amber-600 — ai_estimated
          verified: "#059669", // emerald-600 — assessment_verified
        },

        // ----------------------------------------------------------------
        // Status colours
        // ----------------------------------------------------------------
        status: {
          todo: "#6B7280",
          "in-progress": "#D97706",
          "done-verified": "#059669",
          blocked: "#DC2626",
        },
      },

      // ----------------------------------------------------------------
      // Typography
      // ----------------------------------------------------------------
      fontFamily: {
        sans: ["Inter", "ui-sans-serif", "system-ui", "sans-serif"],
        mono: ["JetBrains Mono", "ui-monospace", "monospace"],
      },

      // ----------------------------------------------------------------
      // Spacing: 4pt / 8pt grid
      // ----------------------------------------------------------------
      spacing: {
        "0.5": "2px",
        "1": "4px",
        "2": "8px",
        "3": "12px",
        "4": "16px",
        "5": "20px",
        "6": "24px",
        "8": "32px",
        "10": "40px",
        "12": "48px",
        "16": "64px",
        "20": "80px",
        "24": "96px",
      },

      // ----------------------------------------------------------------
      // Border radius
      // ----------------------------------------------------------------
      borderRadius: {
        sm: "4px",
        DEFAULT: "8px",
        md: "8px",
        lg: "12px",
        xl: "16px",
        "2xl": "24px",
        full: "9999px",
      },

      // ----------------------------------------------------------------
      // Keyframe animations
      // ----------------------------------------------------------------
      keyframes: {
        "accordion-down": {
          from: { height: "0" },
          to: { height: "var(--radix-accordion-content-height)" },
        },
        "accordion-up": {
          from: { height: "var(--radix-accordion-content-height)" },
          to: { height: "0" },
        },
        "fade-in": {
          from: { opacity: "0", transform: "translateY(4px)" },
          to: { opacity: "1", transform: "translateY(0)" },
        },
      },
      animation: {
        "accordion-down": "accordion-down 0.2s ease-out",
        "accordion-up": "accordion-up 0.2s ease-out",
        "fade-in": "fade-in 0.15s ease-out",
      },
    },
  },
  plugins: [animate],
};

export default config;
