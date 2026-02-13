/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
  theme: {
    extend: {
      colors: {
        brand: {
          50: '#eff6ff',
          100: '#dbeafe',
          200: '#bfdbfe',
          300: '#93c5fd',
          400: '#60a5fa',
          500: '#3b82f6',
          600: '#2563eb',
          700: '#1d4ed8',
          800: '#1e40af',
          900: '#1e3a8a',
        },
        accent: '#6366F1',
        'accent-hover': '#4F46E5',
        'accent-light': '#8B5CF6',
        'accent-text': '#A6ADFF',
        dark: {
          DEFAULT: '#0B0F2F',
          card: '#1E2251',
          lighter: '#0f1338',
          surface: '#1e293b',
        },
        muted: {
          DEFAULT: '#8A93C4',
          light: '#B0B8E0',
        },
      },
      fontFamily: {
        sans: ['Inter', '-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'Roboto', 'Helvetica Neue', 'Arial', 'sans-serif'],
      },
      maxWidth: {
        content: '1200px',
      },
    },
  },
  plugins: [],
};
