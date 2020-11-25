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
                    v-if="$store.state.settings.select_student_by === 'GC'"
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
                    <span slot="noResult">Aucun cours ne correspond à votre recherche.</span>
                </multiselect>
                <multiselect
                    v-else-if="$store.state.settings.select_student_by === 'CL'"
                    :options="classesOptions"
                    placeholder="Cherchez votre classe"
                    select-label=""
                    selected-label="Sélectionné"
                    deselect-label=""
                    label="display"
                    track-by="id"
                    v-model="classe"
                    :show-no-options="false"
                    @input="getStudents"
                    @search-change="searchClasses"
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
                <b-overlay :show="loadingStudent">
                    <b-list-group>
                        <add-absence-entry
                            v-for="s in students"
                            :key="s.matricule"
                            :student="s"
                            @update="computeAlert"
                        />
                    </b-list-group>
                </b-overlay>
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
            classesOptions: [],
            period: null,
            givenCourse: null,
            classe: null,
            students: [],
            showAlert: false,
            currentDate: Moment().format("YYYY-MM-DD"),
            loadingStudent: false,
        };
    },
    methods: {
        computeAlert: function () {
            this.showAlert = Object.keys(this.$store.state.changes).length > 0;
        },
        searchClasses: function (query) {
            const data = {
                query: query,
                check_access: 0,
                teachings: this.$store.state.settings.teachings
            };
            axios.post("/annuaire/api/classes/", data, token)
                .then(resp => {
                    this.classesOptions = resp.data;
                });
        },
        getAbsence: function (students) {
            const data = {
                params: {
                    period: this.period.id,
                    date_absence: this.currentDate,
                    page_size: 5000,
                }
            };
            if (this.$store.state.settings.select_student_by === "GC") data.params.given_course = this.givenCourse.id;
            axios.get("/student_absence_teacher/api/absence/", data, token)
                .then(resp => {
                    console.log(resp.data.results);
                    this.students = students.map(s => {
                        const savedAbsence = resp.data.results.find(r => r.student_id === s.matricule);
                        if (!savedAbsence) return s;

                        s.saved = savedAbsence;
                        return s;
                    });
                    this.loadingStudent = false;
                })
                .catch(err => {
                    alert(err);
                });
        },
        getStudents: function () {
            this.students = [];
            if (this.$store.state.settings.select_student_by === "GC") {
                if (!this.givenCourse || !this.period) return;

                this.loadingStudent = true;
                this.currentDate = Moment().format("YYYY-MM-DD");
                axios.get(`/annuaire/api/student_given_course/${this.givenCourse.id}/`)
                    .then(resp => {
                        this.$store.commit("resetChanges");
                        this.showAlert = 0;
                        this.getAbsence(resp.data);
                    });
            } else if (this.$store.state.settings.select_student_by === "CL") {
                if (!this.classe || !this.period) return;

                this.loadingStudent = true;
                this.currentDate = Moment().format("YYYY-MM-DD");
                const data = {params: {classe: this.classe.id}};
                axios.get("/annuaire/api/studentclasse", data)
                    .then(resp => {
                        this.$store.commit("resetChanges");
                        this.showAlert = 0;
                        this.getAbsence(resp.data);
                    });
            }
        },
        sendChanges: function () {
            const changes = this.$store.state.changes;
            const promises = [];
            for (let matricule in changes) {
                const change = changes[matricule];
                const send = change.is_new ? axios.post : axios.put;
                let url = "/student_absence_teacher/api/absence/";
                if (!change.is_new) url += change.id + "/";
                
                const data = {
                    student_id: matricule,
                    period_id: this.period.id,
                    comment: change.comment,
                    status: change.status
                };
                if (this.$store.state.settings.select_student_by === "GC") data.given_course_id = this.givenCourse.id;
                promises.push(send(url, data, token));
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
        if (this.givenCourseOptions.length > 0 && this.givenCourseOptions[0].display.includes("["))
            return;

        const classesPromises = this.givenCourseOptions.map(givenCourse => {
            return axios.get(`/annuaire/api/course_to_classes/${givenCourse.id}/`);
        });
        Promise.all(classesPromises)
            .then((resps) => {
                resps.forEach((resp, idx) => {
                    let givenCourse = this.givenCourseOptions[idx];
                    givenCourse.display = `[${resp.data.join(", ").toUpperCase()}] ${givenCourse.display}`;
                });
            });
    },
    components: {Multiselect, AddAbsenceEntry,},

};
</script>
