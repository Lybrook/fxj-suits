/** @type {import('tailwindcss').Config} */
export default {
  content: [
      "./app/**/*.{js,ts,jsx,tsx,mdx}",
      "./src/**/*.{js,ts,jsx,tsx,mdx}"
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
          gold:    '#D4B65D',   // Primary accent — FXJ Gold
          dark:    '#17372C',   // Deep dark brown — primary background / text
          mid:     '#27664D',   // Mid-tone gold — secondary elements
          muted:   '#8AA79B',   // Muted gold — subtle accents, borders
          light:   '#F2F1E8',   // Very light gold tint — page backgrounds
          cream:   '#FBFAF6',   // Off-white cream — card backgrounds
        },
      },
      boxShadow: {
        'brand-sm': '0 2px 8px rgba(64, 51, 1, 0.12)',
        'brand-md': '0 4px 20px rgba(64, 51, 1, 0.18)',
        'brand-lg': '0 8px 40px rgba(64, 51, 1, 0.22)',
        'gold':     '0 4px 20px rgba(239, 191, 4, 0.30)',
      },
      backgroundImage: {
        'brand-gradient': 'linear-gradient(135deg, #17372C 0%, #27664D 50%, #17372C 100%)',
        'gold-gradient':  'linear-gradient(135deg, #D4B65D 0%, #8AA79B 100%)',
      },
    },
  },
  plugins: [],
};
