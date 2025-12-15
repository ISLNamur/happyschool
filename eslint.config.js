import js from "@eslint/js";
import stylistic from "@stylistic/eslint-plugin";
import pluginVue from "eslint-plugin-vue";
import globals from "globals";

export default [
    js.configs.recommended,
    stylistic.configs.recommended,
    ...pluginVue.configs["flat/strongly-recommended"],
    {
        plugins: {
            "@stylistic": stylistic,
        },
        languageOptions: {
            ecmaVersion: 2018,
            sourceType: "module",
            globals: {
                ...globals.browser,
            },
        },
        rules: {
            "@stylistic/indent": [
                "error",
                4,
            ],
            "vue/html-indent": [
                "error",
                4,
            ],
            "@stylistic/linebreak-style": [
                "error",
                "unix",
            ],
            "@stylistic/quotes": [
                "error",
                "double",
            ],
            "@stylistic/semi": [
                "error",
                "always",
            ],
            "@stylistic/brace-style": [
                "error",
                "1tbs",
            ],
            "eol-last": [
                "error",
            ],
        },
    },
];
