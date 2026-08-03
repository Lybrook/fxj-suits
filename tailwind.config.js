/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}"
  ],
  darkMode: 'class',
  theme: {
    extend: {
      fontFamily: {
        sans: ['Inter', 'system-ui', '-apple-system', 'sans-serif'],
        serif: ['"Playfair Display"', 'serif'],
      },
      colors: {
        // FXJ Suits Brand Palette
        brand: {
          gold:    '#EFBF04',   // Primary accent — FXJ Gold
          dark:    '#403301',   // Deep dark brown — primary background / text
          mid:     '#856A00',   // Mid-tone gold — secondary elements
          muted:   '#C2B067',   // Muted gold — subtle accents, borders
          light:   '#FDF6DC',   // Very light gold tint — page backgrounds
          cream:   '#FFF9E6',   // Off-white cream — card backgrounds
        },
      },
      boxShadow: {
        'brand-sm': '0 2px 8px rgba(64, 51, 1, 0.12)',
        'brand-md': '0 4px 20px rgba(64, 51, 1, 0.18)',
        'brand-lg': '0 8px 40px rgba(64, 51, 1, 0.22)',
        'gold':     '0 4px 20px rgba(239, 191, 4, 0.30)',
      },
      backgroundImage: {
        'brand-gradient': 'linear-gradient(135deg, #403301 0%, #856A00 50%, #403301 100%)',
        'gold-gradient':  'linear-gradient(135deg, #EFBF04 0%, #C2B067 100%)',
      },
    },
  },
  plugins: [],
};
