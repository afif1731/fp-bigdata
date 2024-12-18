const withMT = require('@material-tailwind/react/utils/withMT')

/** @type {import('tailwindcss').Config} */
const config = {
  content: ['./src/**/*.{js,jsx,ts,tsx}'],
  theme: {
    extend: {
      fontFamily: {
        'montserrat': ['Montserrat'],
      }
    }
  },
  variants: {},
  plugins: ['@tailwindcss/forms']
}

module.exports = withMT(config);