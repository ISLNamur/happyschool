import js from "@eslint/js";
import pluginVue from "eslint-plugin-vue";
import globals from "globals";

export default [
    js.configs.recommended,
    ...pluginVue.configs["flat/strongly-recommended"],
    {
        languageOptions: {
            ecmaVersion: 2018,
            sourceType: "module",
            globals: {
                ...globals.browser,
                myCustomGlobal: "readonly"
            }
        },
        "rules": {
            "indent": [
                "error",
                4
            ],
            "vue/html-indent": [
                "error",
                4
            ],
            "linebreak-style": [
                "error",
                "unix"
            ],
            "quotes": [
                "error",
                "double"
            ],
            "semi": [
                "error",
                "always"
            ],
            "eol-last": [
                "error",
            ],
        }
    }
];
