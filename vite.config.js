import { globSync } from "glob";

import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import { djangoVitePlugin } from "django-vite-plugin";

import Components from "unplugin-vue-components/vite";
import {BootstrapVueNextResolver} from "bootstrap-vue-next";

import Icons from "unplugin-icons/vite";
import IconsResolver from "unplugin-icons/resolver";

// Look for apps
const appPathStartPoint = globSync("*/static/*/js/*.js");
// Remove */static/
const appPathTruncate = appPathStartPoint.map(p => p.split("/").slice(2, 5).join("/"));
console.log("App found", appPathTruncate);

export default defineConfig({
    plugins: [
        vue(),
        Components({
            resolvers: [BootstrapVueNextResolver(), IconsResolver()],
        }),
        Icons(),
        djangoVitePlugin(appPathTruncate),
    ],
    build: {
        emptyOutDir: false,
    },
});
