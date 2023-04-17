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

const token = { xsrfCookieName: "csrftoken", xsrfHeaderName: "X-CSRFToken" };

export default new Vuex.Store({
    state: {
        // eslint-disable-next-line no-undef
        settings: settings,
        filters: [{
            filterType: "activate_ongoing",
            tag: "Activer",
            value: true,
        }],
        changeType: [],
        changeCategory: [],
        places: [],
        // eslint-disable-next-line no-undef
        canAdd: can_add,
        ready: false,
    },
    actions: {
        getChangeType (context) {
            axios.get("/schedule_change/api/schedule_change_type/", token)
                .then(resp => {
                    context.commit("setChangeType", resp.data.results);
                });
        },
        getChangeCategory (context) {
            axios.get("/schedule_change/api/schedule_change_category/", token)
                .then(resp => {
                    context.commit("setChangeCategory", resp.data.results);
                });
        },
        getPlaces (context) {
            return new Promise(resolve => {
                if (context.state.places.length > 0) {
                    resolve();
                } else {
                    axios.get("/schedule_change/api/schedule_change_place/")
                        .then(resp => {
                            context.state.places = resp.data.results.map(p => p.name);
                            resolve();
                        });
                }
            });
        }
    },
    mutations: {
        enableFullscreen: function (state) {
            state.canAdd = false;
            this.commit("addFilter", {filterType: "activate_has_classe", tag: "Activer", value: true});
        },
        setChangeType: function (state, types) {
            state.changeType = types;
        },
        setChangeCategory: function (state, categories) {
            state.changeCategory = categories;
            state.ready = true;

            // Add style.
            var sheet = document.createElement("style");
            for (let c in categories) {
                sheet.innerHTML +=  ".category-" + categories[c].id + " {background-color: #" + categories[c].color + "60;} ";
            }
            document.body.appendChild(sheet);
        },
        addFilter: function (state, filter) {
            // If filter is a matricule, remove name filter to avoid conflict.
            if (filter.filterType === "matricule_id") {
                this.commit("removeFilter", "name");
            }

            // Overwrite same filter type.
            this.commit("removeFilter", filter.filterType);

            state.filters.push(filter);
        },
        removeFilter: function (state, key) {
            for (let f in state.filters) {
                if (state.filters[f].filterType === key) {
                    state.filters.splice(f, 1);
                    break;
                }
            }
        },
    },
});
