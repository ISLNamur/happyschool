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
        <b-row>
            <b-col cols="2">
                <p class="pt-1">
                    <strong>{{ currentDate }}</strong>
                </p>
            </b-col>
            <b-col>
                <multiselect
                    :options="periodOptions"
                    placeholder="Séléctionner une période de cours"
                    select-label=""
                    selected-label="Sélectionné"
                    deselect-label=""
                    label="display"
                    track-by="id"
                    v-model="period"
                    :show-no-options="false"
                    @input="getStudents"
                >
                    <span slot="noResult">Aucune période ne correspond à votre recherche.</span>
                </multiselect>
            </b-col>
            <b-col>
                <multiselect
                    :options="givenCourseOptions"
                    placeholder="Séléctionner votre cours"
                    select-label=""
                    selected-label="Sélectionné"
                    deselect-label=""
                    label="display"
                    track-by="id"
                    v-model="givenCourse"
                    :show-no-options="false"
                    @input="getStudents"
                >
                    <span slot="noResult">Aucune classe ne correspond à votre recherche.</span>
                </multiselect>
            </b-col>
        </b-row>
        <b-row class="mt-2">
            <b-col cols="3">
                <b-btn
                    @click="sendChanges"
                    :disabled="!showAlert"
                >
                    Valider les changements
                </b-btn>
            </b-col>
            <b-col>
                <b-alert
                    :show="showAlert"
                    variant="warning"
                >
                    Il y a des changements non-validés !
                </b-alert>
            </b-col>
        </b-row>
        <b-row class="mt-2">
            <b-col>
                <b-list-group>
                    <add-absence-entry
                        v-for="s in students"
                        :key="s.matricule"
                        :student="s"
                        @update="computeAlert"
                    />
                </b-list-group>
            </b-col>
        </b-row>
    </div>
</template>

<script>
import Multiselect from "vue-multiselect";
import "vue-multiselect/dist/vue-multiselect.min.css";

import axios from "axios";
import Moment from "moment";

import AddAbsenceEntry from "./add_absence_entry.vue";

const token = {xsrfCookieName: "csrftoken", xsrfHeaderName: "X-CSRFToken"};

export default {
    data: function () {
        return {
            periodOptions: [],
            givenCourseOptions: [],
            period: null,
            givenCourse: null,
            students: [],
            showAlert: false,
            currentDate: Moment().format("YYYY-MM-DD")
        };
    },
    methods: {
        computeAlert: function () {
            this.showAlert = Object.keys(this.$store.state.changes).length > 0;
        },
        promiseSavedData: function (model) {
            const data = {
                params: {
                    period: this.period.id,
                    given_course: this.givenCourse.id,
                    [`date_${model}`]: this.currentDate,
                }
            };
            return axios.get(`/student_absence_teacher/api/${model}/`, data, token);
        },
        getAbsenceLateness: function (students) {
            // We need both the given course and the period.
            if (!this.period || !this.givenCourse) return;

            const models = ["absence", "lateness"];
            Promise.all([this.promiseSavedData(models[0]), this.promiseSavedData(models[1])])
                .then(resps => {
                    for (let resp in resps) {
                        for (let r in resps[resp].data.results) {
                            const object = resps[resp].data.results[r];
                            object.choice = models[resp];
                            for (let s in students) {
                                if (students[s].matricule == object.student_id) {
                                    students[s]["saved"] = object;
                                    break;
                                }
                            }
                        }
                    }
                    this.students = students;
                })
                .catch(err => {
                    alert(err);
                });
        },
        getStudents: function () {
            this.students = [];
            if (!this.givenCourse || !this.period) return;

            this.currentDate = Moment().format("YYYY-MM-DD");
            axios.get(`/annuaire/api/student_given_course/${this.givenCourse.id}/`)
                .then(resp => {
                    this.$store.commit("resetChanges");
                    this.showAlert = 0;
                    this.getAbsenceLateness(resp.data);
                });

        },
        sendChanges: function () {
            const changes = this.$store.state.changes;
            const promises = [];
            for (let matricule in changes) {
                const change = changes[matricule];
                if (("old_choice" in change && change.old_choice != change.choice)
                    || change.choice == "presence") {
                    promises.push(axios.delete(`/student_absence_teacher/api/${change.old_choice}/${change.id}/`, token));
                }

                if (change.choice != "presence") {
                    const send = change.is_new ? axios.post : axios.put;
                    let url = "/student_absence_teacher/api/" + change.choice + "/";
                    if (!change.is_new) url += change.id + "/";
                    const data = {
                        student_id: matricule,
                        given_course_id: this.givenCourse.id,
                        period_id: this.period.id,
                        comment: change.comment,
                    };
                    promises.push(send(url, data, token));
                }
            }
            Promise.all(promises)
                .then(resps => {
                    for (let r in resps) {
                        this.$store.commit("removeChange", resps[r].data.student_id);
                    }
                    this.$bvToast.toast("Les changements ont été sauvés.", {
                        variant: "success",
                        noCloseButton: true,
                    });
                    this.getStudents();
                    this.computeAlert();
                })
                .catch(err => {
                    alert(err);
                });
        }
    },
    mounted: function () {
        axios.get("/student_absence_teacher/api/period/")
            .then(resp => {
                this.periodOptions = resp.data.results;
            });
        // eslint-disable-next-line no-undef
        this.givenCourseOptions = user_properties.given_courses;
        const classesPromises = this.givenCourseOptions.map(givenCourse => {
            return axios.get(`/annuaire/api/course_to_classes/${givenCourse.id}/`)
        });
        Promise.all(classesPromises)
            .then((resps) => {
                resps.forEach((resp, idx) => {
                    console.log(resp.data);
                    let givenCourse = this.givenCourseOptions[idx];
                    givenCourse.display = `[${resp.data.join(", ").toUpperCase()}] ${givenCourse.display}`;
                });
            });
    },
    components: {Multiselect, AddAbsenceEntry,},

};
</script>
