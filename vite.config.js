import { globSync } from "glob"

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { djangoVitePlugin } from 'django-vite-plugin'

// Look for apps
const appPathStartPoint = globSync("*/static/*/js/*.js");
// Remove */static/
const appPathTruncate = appPathStartPoint.map(p => p.split("/").slice(2, 5).join("/"));
console.log("App found", appPathTruncate);

export default defineConfig({
  resolve: {
    alias: {
      vue: '@vue/compat'
    }
  },
  plugins: [
    vue({
      template: {
        compilerOptions: {
          compatConfig: {
            MODE: 2
          }
        }
      }
    }),
    djangoVitePlugin(appPathTruncate),
  ],
})
