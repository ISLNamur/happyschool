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

import axios from "axios";

import { defineStore } from "pinia";

import { addFilterPinia as addFilter, removeFilterPinia as removeFilter } from "@s:core/js/common/filters.js";

const token = { xsrfCookieName: "csrftoken", xsrfHeaderName: "X-CSRFToken" };

export const scheduleChangeStore = defineStore("scheduleChangeStore", {
    state: () => ({
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
        lastPage: null,
    }),
    actions: {
        getChangeType () {
            axios.get("/schedule_change/api/schedule_change_type/", token)
                .then(resp => {
                    this.setChangeType(resp.data.results);
                });
        },
        getChangeCategory () {
            axios.get("/schedule_change/api/schedule_change_category/", token)
                .then(resp => {
                    this.setChangeCategory(resp.data.results);
                });
        },
        getPlaces () {
            return new Promise(resolve => {
                if (this.places.length > 0) {
                    resolve();
                } else {
                    axios.get("/schedule_change/api/schedule_change_place/")
                        .then(resp => {
                            this.places = resp.data.results.map(p => p.name);
                            resolve();
                        });
                }
            });
        },
        addFilter,
        removeFilter,
        updatePage (page) {
            this.lastPage = page;
        },
        enableFullscreen: function () {
            this.canAdd = false;
            this.addFilter({filterType: "activate_has_classe", tag: "Activer", value: true});
        },
        setChangeType: function (types) {
            this.changeType = types;
        },
        setChangeCategory: function (categories) {
            this.changeCategory = categories;
            this.ready = true;

            // Add style.
            var sheet = document.createElement("style");
            for (let c in categories) {
                sheet.innerHTML +=  ".category-" + categories[c].id + " {background-color: #" + categories[c].color + "60;} ";
            }
            document.body.appendChild(sheet);
        },
    },
});
