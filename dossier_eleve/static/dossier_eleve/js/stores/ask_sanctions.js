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

import axios from "axios";

import { defineStore } from "pinia";

import { addFilterPinia as addFilter, removeFilterPinia as removeFilter } from "@s:core/js/common/filters.js";

export const askSanctionsStore = defineStore("askSanctionsStore", {
    state: () => ({

        settings: settings,
        filters: [
            {
                filterType: "scholar_year",

                tag: currentYear,

                value: currentYear,
            },
            {
                filterType: "activate_own_classes",
                tag: true,
                value: true,
            },
        ],

        canSetSanction: canSetSanction,

        canAskSanction: canAskSanction,

        hasProEco: proeco,
        sanctions: [],
    }),
    actions: {
        addFilter: addFilter,
        removeFilter: removeFilter,
        getSanctions: function () {
            return new Promise((resolve) => {
                if (this.sanctions.length == 0) {
                    axios.get("/dossier_eleve/api/sanction_decision/?only_sanctions=1")
                        .then((resp) => {
                            this.sanctions = resp.data.results;
                            resolve();
                        });
                } else {
                    resolve();
                }
            });
        },
    },
});
