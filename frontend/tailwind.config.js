/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: '#0066FF',
        secondary: '#00C853',
        danger: '#FF3D00',
        dark: '#1A1A2E',
        light: '#F5F7FA',
        gold: '#FFD700',
      },
    },
  },
  plugins: [],
}
