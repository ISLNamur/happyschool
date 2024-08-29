<!-- This file is part of Happyschool. -->
<!--  -->
<!-- Happyschool is the legal property of its developers, whose names -->
<!-- can be found in the AUTHORS file distributed with this source -->
<!-- distribution. -->
<!--  -->
<!-- Happyschool is free software: you can redistribute it and/or modify -->
<!-- it under the terms of the GNU Affero General Public License as published by -->
<!-- the Free Software Foundation, either version 3 of the License, or -->
<!-- (at your option) any later version. -->
<!--  -->
<!-- Happyschool is distributed in the hope that it will be useful, -->
<!-- but WITHOUT ANY WARRANTY; without even the implied warranty of -->
<!-- MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the -->
<!-- GNU Affero General Public License for more details. -->
<!--  -->
<!-- You should have received a copy of the GNU Affero General Public License -->
<!-- along with Happyschool.  If not, see <http://www.gnu.org/licenses/>. -->

<template>
    <div>
        <div
            class="loading"
            v-if="!loaded"
        />
        <app-menu
            v-if="loaded"
            :menu-info="menuInfo"
        />
        <b-container v-if="loaded">
            <h1>Absence des élèves</h1>
            <b-row class="mb-1">
                <b-nav tabs>
                    <b-nav-item
                        to="/add_absence"
                        v-if="can_access_adding"
                    >
                        <b-icon
                            icon="plus"
                            color="green"
                            scale="1.5"
                            class="border"
                        />
                        Ajouter absenses/retards
                    </b-nav-item>
                    <b-nav-item
                        to="/add_exclusion"
                        v-if="can_access_exclusion"
                    >
                        <b-icon
                            icon="plus"
                            color="green"
                            scale="1.5"
                            class="border"
                        />
                        Ajouter exclusion
                    </b-nav-item>
                    <b-nav-item
                        v-if="can_access_list"
                        :to="`/overview/${date}/`"
                    >
                        Vue d'ensemble
                    </b-nav-item>
                    <b-nav-item
                        v-if="can_access_list"
                        :to="`/justification/`"
                    >
                        Justificatifs
                    </b-nav-item>
                    <b-nav-item
                        v-if="can_access_adding"
                        to="/export"
                    >
                        Export
                    </b-nav-item>
                </b-nav>
            </b-row>
            <router-view />
        </b-container>
    </div>
</template>

<script>
import Vue from "vue";
import { BootstrapVue, BootstrapVueIcons } from "bootstrap-vue";
import "bootstrap-vue/dist/bootstrap-vue.css";

Vue.use(BootstrapVue);
Vue.use(BootstrapVueIcons);

import Moment from "moment";
Moment.locale("fr");

import Menu from "@s:core/js/common/menu_bar.vue";

import { studentAbsenceTeacherStore } from "./stores/index.js";

export default {
    data: function () {
        return {
            menuInfo: {},
            loaded: false,
            store: studentAbsenceTeacherStore()
        };
    },
    computed: {
        date: function () {
            if ("date" in this.$route.params) {
                return this.$route.params.date;
            }

            return Moment().format("YYYY-MM-DD");
        },
        can_access_list: function () {
            const access_groups = this.store.settings.can_see_list;
            for (let ag in this.store.settings.can_see_list) {
                // eslint-disable-next-line no-undef
                for (let g in user_groups) {
                    // eslint-disable-next-line no-undef
                    if (user_groups[g].id == access_groups[ag]) return true;
                }
            }
            return false;
        },
        can_access_adding: function () {
            const access_groups = this.store.settings.can_see_adding;
            for (let ag in this.store.settings.can_see_adding) {
                // eslint-disable-next-line no-undef
                for (let g in user_groups) {
                    // eslint-disable-next-line no-undef
                    if (user_groups[g].id == access_groups[ag]) return true;
                }
            }
            return false;
        },
        can_access_exclusion: function () {
            const access_groups = this.store.settings.can_see_exclusion;
            for (let ag in this.store.settings.can_see_exclusion) {
                // eslint-disable-next-line no-undef
                for (let g in user_groups) {
                    // eslint-disable-next-line no-undef
                    if (user_groups[g].id == access_groups[ag]) return true;
                }
            }
            return false;
        }
    },
    beforeMount: function () {
        // Move to overview if not having adding access.
        if (!this.can_access_adding && this.can_access_list) {
            if (
                this.$router.currentRoute.value.fullPath.includes("add_absence")
                || this.$router.currentRoute.value.path === "/"
            ) {
                this.$router.push(`/overview/${this.date}`);
            }

        }
    },
    mounted: function () {
        // eslint-disable-next-line no-undef
        this.menuInfo = menu;
        this.loaded = true;
    },
    components: {
        "app-menu": Menu,
    }
};
</script>
