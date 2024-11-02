import globals from "globals";
import js from "@eslint/js";

export default [
  js.configs.recommended,
  {
    languageOptions: {
      ecmaVersion: 2022,
      sourceType: "module",
      globals: {
        ...globals.browser,
        ...globals.node,
      },
    },
    rules: {
      // Common rules
      semi: ["error", "always"],
      quotes: ["error", "double"],
      "no-unused-vars": "warn",
      "no-console": "warn",

      // Error prevention
      "no-undef": "error",
      "no-var": "error",
      "prefer-const": "error",

      // Style
      indent: ["error", 4],
      "max-len": ["error", { code: 100 }],
      "comma-dangle": ["error", "always-multiline"],
    },
  },
];
