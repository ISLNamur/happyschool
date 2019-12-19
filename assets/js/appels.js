// This file is part of Happyschool.
//
// Happyschool is the legal property of its developers, whose names
// can be found in the AUTHORS file distributed with this source
// distribution.
//
// Happyschool is free software: you can redistribute it and/or modify
// it under the terms of the GNU Affero General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
//
// Happyschool is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU Affero General Public License for more details.
//
// You should have received a copy of the GNU Affero General Public License
// along with Happyschool.  If not, see <http://www.gnu.org/licenses/>.

import Vue from "vue";

import Vuex from "vuex";
Vue.use(Vuex);

import axios from "axios";
import router from "../appels/router.js";
import Menu from "../common/menu.vue";

const store = new Vuex.Store({
    state: {
        // eslint-disable-next-line no-undef
        settings: settings,
        filters: [{
            filterType: "activate_ongoing",
            tag: "Activer",
            value: true,
        }],
        emails: [],
    },
    mutations: {
        addFilter: function(state, filter) {
            // If filter is a matricule, remove name filter to avoid conflict.
            if (filter.filterType === "matricule_id") {
                this.commit("removeFilter", "name");
            }

            // Overwrite same filter type.
            this.commit("removeFilter", filter.filterType);

            state.filters.push(filter);
        },
        removeFilter: function(state, key) {
            for (let f in state.filters) {
                if (state.filters[f].filterType === key) {
                    state.filters.splice(f, 1);
                    break;
                }
            }
        },
        setEmails: function(state, emails) {
            state.emails = emails;
        },
    },
    actions: {
        loadEmails(context) {
            const token = { xsrfCookieName: "csrftoken", xsrfHeaderName: "X-CSRFToken" };
            axios.get("/core/api/email/", token)
                .then(response => {
                    context.commit("setEmails", response.data.results);
                });
        }
    }
});

store.dispatch("loadEmails");



new Vue({
    el: "#vue-app",
    data: {
        menuInfo: {},
        transitionName: "slide-left",
    },
    store,
    router,
    template: `
    <div>
      <app-menu :menu-info="menuInfo"></app-menu>
      <transition :name="transitionName" mode="out-in">
        <router-view></router-view>
      </transition>
    </div>`,
    mounted: function() {
        // eslint-disable-next-line no-undef
        this.menuInfo = menu;
    },
    components: {
        "app-menu": Menu,
    },
    watch: {
        "$route" (to, from) {
            const toDepth = to.path.split("/").length;
            const fromDepth = from.path.split("/").length;
            this.transitionName = toDepth < fromDepth ? "slide-right" : "slide-left";
        }
    }
});
