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

/**
 * Store the state locally in order to have offline access.
 */
const vuexLocal = new VuexPersistence({
    storage: window.localStorage,
    reducer: (state) => {
        // Initially set the settings to allow further updates.
        // eslint-disable-next-line no-undef
        state["settings"] = settings;
        return state;
    },
});

const token = { xsrfCookieName: "csrftoken", xsrfHeaderName: "X-CSRFToken" };

export default new Vuex.Store({
    state: {
        /**
         * The global settings for the student absence app.
         */
        // eslint-disable-next-line no-undef
        settings: settings,
        /**
         * Filters in use for absences list.
         */
        filters: [],
        /**
         * Absences (or attendances) already saved on the server.
         */
        savedAbsences: {},
        /**
         * Local absences (or attendances), not saved on the server.
         */
        changes: [],
        /**
         * Notes about a class.
         */
        notes: {},
        /**
         * State if there is a connection to the server.
         */
        onLine: true,
        /**
         * The last date and time the list of students and classes where updated
         * from the server.
         */
        lastUpdate: "",
        /**
         * State if the application is currently updating.
         */
        updating: false,
        /**
         * State if the restriction by classes is bypassed.
         */
        forceAllAccess: false,
        /**
         * The list of periods a normal day has.
         */
        periods: []
    },
    getters: {
        /**
         * Get a specific local change from a matricule, a date and a period.
         * @param {Object} absence An object including the searched `matricule`,
         * `date_absence` and `period`.
         */
        change: (state) => (absence) => {
            const curChange = state.changes.find(change => {
                return change.matricule == absence.matricule
                    && change.date_absence == absence.date_absence
                    && change.period == absence.period;
            });
            if (curChange) return curChange;

            return null;
        },
        /**
         * Get a specific saved change (already on the server) from a matricule,
         * a date and a period.
         * @param {Object} absence An object including the searched `matricule`,
         * `date_absence` and `period`.
         */
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
        /**
         * Assign periods.
         * @param {Array} periods A list of period objects.
         */
        setPeriods: function (state, periods) {
            state.periods = periods;
        },
        /**
         * Toggle restriction by class/year for classes.
         */
        toggleForceAllAccess: function (state) {
            state.forceAllAccess = !state.forceAllAccess;
            this.commit("updateStudentsClasses");
        },
        /**
         * Add a note to the store.
         * @param {Object} note A note object.
         */
        addNote: function (state, note) {
            state.notes[note.classe] = note;
        },
        /**
         * Add a filter to the list of absences.
         */
        addFilter: addFilter,
        /**
         * Remove a filter to the list of absences.
         */
        removeFilter: removeFilter,
        /**
         * Remove a local change.
         * @param {Object} change The change to be removed. It must contain the `matricule`,
         * `date_absence` and `period`.
         */
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
        /**
         * Add a local change.
         * @param {*} change The new change must contain the `matricule`, `date_absence`
         * and `period`.
         */
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
        /**
         * Assign absences stated as saved on the server to the store.
         * @param {*} absences A list of absences.
         */
        setSavedAbsences: function (state, absences) {
            for (let a in absences) {
                if ("student" in absences[a]) delete absences[a].student.savedAbsence.student.savedAbsence;
            }
            state.savedAbsences = absences;
        },
        /**
         * Download and update saved absences from today.
         * @param {String} date The date of the absences to get.
         */
        updateSavedAbsences: function (state, date) {
            let url = "/student_absence/api/student_absence/?page_size=1000&";
            url += "forceAllAccess=" + state.forceAllAccess + "&";
            url += "date_absence=" + date;
            return axios.get(url, token)
                .then(resp => {
                    state.savedAbsences = resp.data.results;
                    return state.savedAbsences;
                });
        },
        /**
         * Download from the server and update the classes and students on the store.
         */
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
                    setTimeout(() => {
                        document.location.reload(true);
                    }, 500);
                });
            axios.get("/student_absence/api/classenote/", token)
                .then(response => {
                    for (let n in response.data.results) {
                        this.commit("addNote", response.data.results[n]);
                    }
                });
        },
        /**
         * Set the updating status. 
         * @param {Boolean} updating The update status.
         */
        updatingStatus: function (state, updating) {
            state.updating = updating;
        },
        /**
         * Set the online status.
         * @param {Boolean} onLine The online status.
         */
        changeOnLineStatus: function (state, onLine) {
            state.onLine = onLine;
        }
    },
    plugins: [vuexLocal.plugin],
});
