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

export const studentAbsenceTeacherStore = defineStore("studentAbsenceTeacher", {
    state: () => ({
        // eslint-disable-next-line no-undef
        settings: settings,
        filters: [],
        changes: {},
        periodEduc: [],
        motives: [],
    }),
    actions: {
        addFilter: addFilter,
        removeFilter: removeFilter,
        setChange: function (change) {
            this.changes[change.matricule] = change;
        },
        removeChange: function (matricule) {
            if (matricule in this.changes) delete this.changes[matricule];
        },
        resetChanges: function (resetExceptions) {
            if (resetExceptions) {
                const keepChanges = Object.entries(this.changes).filter(
                    (change) => resetExceptions.includes(change[1].matricule)
                );
                this.changes = Object.fromEntries(keepChanges);
                return;
            }
            this.changes = {};
        },
        getOptions: function () {
            return new Promise((resolve, reject) => {
                Promise.all([
                    axios.get("/student_absence_teacher/api/period_educ/"),
                    axios.get("/student_absence_teacher/api/just_motive/"),
                ]).then((resps) => {
                    this.periodEduc = resps[0].data.results;
                    this.periodEduc.forEach((v, i) => {
                        v.index = i;
                    });

                    this.motives = resps[1].data.results;

                    resolve();
                }).catch((err) => {
                    console.log(err);
                    reject();
                });
            });
        }
    }
});
