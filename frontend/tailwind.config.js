module.exports = {
  purge: ["../webapp/webapp/templates/**/*.html", "../webapp/webapp/templates/**/*.j2"],
  darkMode: false, // or 'media' or 'class'
  theme: {
    extend: {
      transitionProperty: {
        'max-height': 'max-height'
      }
    }
  }
,
  variants: {
    extend: {
    },
  },
  plugins: [],
};
