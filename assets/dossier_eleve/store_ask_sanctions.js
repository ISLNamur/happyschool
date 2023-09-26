
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

/* eslint-disable no-undef */

import Vue from "vue";
import Vuex from "vuex";

import {addFilter, removeFilter} from "../common/filters.js";

Vue.use(Vuex);

export default new Vuex.Store({
    state: {
        // eslint-disable-next-line no-undef
        settings: settings,
        filters: [
            {
                filterType: "scholar_year",
                // eslint-disable-next-line no-undef
                tag: currentYear,
                // eslint-disable-next-line no-undef
                value: currentYear,
            },
            {
                filterType: "activate_own_classes",
                tag: true,
                value: true,
            },
        ],
        // eslint-disable-next-line no-undef
        canSetSanction: canSetSanction,
        // eslint-disable-next-line no-undef
        canAskSanction: canAskSanction,
        // eslint-disable-next-line no-undef
        hasProEco: proeco,
        sanctions: [],
    },
    mutations: {
        addFilter: addFilter,
        removeFilter: removeFilter,
    },
    actions: {
        getSanctions: function (context) {
            return new Promise(resolve => {
                if (context.state.sanctions.length == 0) {
                    axios.get("/dossier_eleve/api/sanction_decision/?only_sanctions=1")
                        .then(resp => {
                            context.state.sanctions = resp.data.results;
                            resolve();
                        });
                } else {
                    resolve();
                }
            });
        }
    },
});
