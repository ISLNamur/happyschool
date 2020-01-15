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
import VuexPersistence from "vuex-persist";

import axios from "axios";

import Moment from "moment";
Moment.locale("fr");

import {addFilter, removeFilter} from "../common/filters.js";

Vue.use(Vuex);

const vuexLocal = new VuexPersistence({
    storage: window.localStorage,
    reducer: (state) => {
        // eslint-disable-next-line no-undef
        state["settings"] = settings;
        return state;
    },
});

const token = { xsrfCookieName: "csrftoken", xsrfHeaderName: "X-CSRFToken" };

export default new Vuex.Store({
    state: {
        // eslint-disable-next-line no-undef
        settings: settings,
        filters: [],
        savedAbsences: {},
        changes: [],
        notes: {},
        onLine: true,
        lastUpdate: "",
        updating: false,
        forceAllAccess: false,
        periods: []
    },
    getters: {
        change: (state) => (absence) => {
            const curChange = state.changes.find(change => {
                return change.matricule == absence.matricule
                    && change.date_absence == absence.date_absence
                    && change.period == absence.period;
            });
            if (curChange) return curChange;

            return null;
        },
        savedAbsence(state) {
            return absence => {
                const absenceFound = state.savedAbsences.find(sAbs => {
                    const isStudent = sAbs.student_id == absence.matricule;
                    const isCurrentDate = sAbs.date_absence == absence.date_absence;
                    const isGoodPeriod = sAbs.period == absence.period;
                    return isStudent && isCurrentDate && isGoodPeriod;
                });
                if (absenceFound) return absenceFound;

                return null;
            };
        }
    },
    mutations: {
        setPeriods: function (state, periods) {
            state.periods = periods;
        },
        toggleForceAllAccess: function (state) {
            state.forceAllAccess = !state.forceAllAccess;
            this.commit("updateStudentsClasses");
        },
        addNote: function (state, note) {
            state.notes[note.classe] = note;
        },
        addFilter: addFilter,
        removeFilter: removeFilter,
        removeChange: function (state, change) {
            for (let c in state.changes) {
                if (state.changes[c].matricule == change.matricule
                    && state.changes[c].date_absence == change.date_absence
                    && state.changes[c].period == change.period) {
                    state.changes.splice(c, 1);
                    break;
                }
            }
        },
        setChange: function (state, change) {
            let oldChange = null;
            for (let c in state.changes) {
                if (state.changes[c].matricule == change.matricule
                    && state.changes[c].date_absence == change.date_absence
                    && state.changes[c].period == change.period) {
                    state.changes[c].index = c;
                    oldChange = state.changes[c];
                    break;
                }
            }

            if (!oldChange) {
                state.changes.push(change);
            } else {
                state.changes[oldChange.index].is_absent = change.is_absent;
                // Force update.
                Vue.set(state.changes, oldChange.index, state.changes[oldChange.index]);
            }
        },
        setSavedAbsences: function (state, absences) {
            for (let a in absences) {
                if ("student" in absences[a]) delete absences[a].student.savedAbsence.student.savedAbsence;
            }
            state.savedAbsences = absences;
        },
        /**
         * Download and update saved absences from today.
         * @param {Object} state The state of the store.
         * @param {String} date The date of the absences to get.
         */
        updateSavedAbsences: function (state, date) {
            return axios.get("/student_absence/api/student_absence/?page_size=1000&date_absence=" + date, token)
                .then(resp => {
                    state.savedAbsences = resp.data.results;
                    return state.savedAbsences;
                });
        },
        updateStudentsClasses: function (state) {
            state.lastUpdate = Moment().format("YYYY-MM-DD");
            this.commit("updatingStatus", true);
            const filterForEduc = state.settings.filter_students_for_educ;
            const data = {
                query: "everybody",
                teachings: state.settings.teachings,
                people: "student",
                active: true,
                check_access:  filterForEduc != "none" && !state.forceAllAccess,
                educ_by_years: filterForEduc == "year" && !state.forceAllAccess,
            };
            axios.post("/student_absence/api/students_classes/", data, token)
                .then(() => {
                    this.commit("updatingStatus", false);
                    document.location.reload(true);
                });
            axios.get("/student_absence/api/classenote/", token)
                .then(response => {
                    for (let n in response.data.results) {
                        this.commit("addNote", response.data.results[n]);
                    }
                });
        },
        updatingStatus: function (state, updating) {
            state.updating = updating;
        },
        changeOnLineStatus: function (state, onLine) {
            state.onLine = onLine;
        }
    },
    plugins: [vuexLocal.plugin],
});
