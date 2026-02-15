/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#F59E0B',
          dark: '#D97706',
          light: '#FBBF24',
        },
        dark: {
          DEFAULT: '#0D0B08',
          glass: 'rgba(255,255,255,0.04)',
        },
        glass: {
          border: 'rgba(251, 191, 36, 0.08)',
        },
      },
      fontFamily: {
        sans: ['Inter', '-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'sans-serif'],
      },
      backdropBlur: {
        glass: '20px',
      },
      borderRadius: {
        glass: '16px',
      },
      minHeight: {
        touch: '48px',
      },
      minWidth: {
        touch: '48px',
      },
    },
  },
  plugins: [],
}
