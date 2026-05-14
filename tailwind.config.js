/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        primary: '#10b981', // Emerald 500
        secondary: '#3b82f6', // Blue 500
        lightBlue: '#e0f2fe',
        dark: '#1e293b',
      },
      fontFamily: {
        sans: ['Tajawal', 'sans-serif'],
      }
    },
  },
  plugins: [],
}
