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
// const appPathTruncate = appPathStartPoint.map(p => p.split("/").slice(2, 5).join("/"));
// console.log("App found", appPathTruncate);

const appPathTruncate = [
    "student_absence_teacher/js/student_absence_teacher.js",
    "schedule_change/js/schedule_change.js",
    // 'pia/js/pia.js',
    "mail_notification/js/mail_notification.js",
    // 'lateness/js/lateness.js',
    // 'inscription/js/inscription.js',
    "infirmerie/js/infirmerie.js",
    // 'home/js/home.js',
    // 'grandset/js/grandset.js',
    "dossier_eleve/js/dossier_eleve.js",
    "dossier_eleve/js/ask_sanctions.js",
    // 'core/js/members.js',
    "core/js/auth.js",
    // 'core/js/admin.js',
    "appels/js/appels.js",
    "annuaire/js/annuaire.js",
    "absence_prof/js/absence_prof.js"
];

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
