/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html",
    "./static/src/**/*.js"
  ],
  theme: {
    extend: {
      fontFamily: {
        "poppins": ["Poppins", "sans-serif"],
        "nunito": ["Nunito", "sans-serif"]
      },
      colors: {
        "dark": "#161616",
        "green": "#096264",
        "green100": "#009598",
        "gold": "#8C673B",
        "gold100": "#DB9D54",
        "white10": "rgba(255, 255, 255, 0.1)",
        "white20": "rgba(255, 255, 255, 0.2)",
        "gray": "#BCBCBC",
      }
    },
  },
  plugins: [],
}

