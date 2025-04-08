/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'primary-bg': '#1a2b59',
        'secondary-bg': '#1e3275',
        'card-bg': '#243980',
        'text-color': '#ffffff',
        'chart-bar-color': '#39a0ff',
        'chart-line-color': '#ffde33',
        'hover-color': '#2c4390',
      },
    },
  },
  plugins: [],
} 