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
            <b-col
                cols="12"
                md="4"
                lg="3"
            >
                <b-form-group>
                    <b-input
                        v-model="currentDate"
                        type="date"
                        @change="getStudents('UND')"
                    />
                </b-form-group>
            </b-col>
            <b-col
                cols="12"
                md="6"
                lg="3"
            >
                <multiselect
                    :options="periodOptions"
                    placeholder="Séléctionner une période"
                    select-label=""
                    selected-label="Sélectionné"
                    deselect-label="Déselectionner"
                    label="display"
                    track-by="id"
                    v-model="period"
                    :show-no-options="false"
                    :multiple="true"
                    @input="getStudents('UND', true)"
                    class="mb-1"
                >
                    <template #noResult>
                        Aucune période ne correspond à votre recherche.
                    </template>
                </multiselect>
            </b-col>
            <b-col
                cols="12"
                md="6"
                lg="3"
            >
                <multiselect
                    v-if="store.settings.select_student_by === 'GC' || store.settings.select_student_by === 'CLGC'"
                    :options="givenCourseOptions"
                    placeholder="Séléctionner votre cours"
                    select-label=""
                    selected-label="Sélectionné"
                    deselect-label=""
                    label="display"
                    track-by="id"
                    v-model="givenCourse"
                    :show-no-options="false"
                    @input="getStudents('GC')"
                    class="mb-1"
                >
                    <template #noResult>
                        Aucun cours ne correspond à votre recherche.
                    </template>
                </multiselect>
            </b-col>
            <span v-if="store.settings.select_student_by === 'CLGC'">ou</span>
            <b-col>
                <multiselect
                    v-if="store.settings.select_student_by === 'CL' || store.settings.select_student_by === 'CLGC'"
                    :options="classesOptions"
                    placeholder="Chercher une classe"
                    select-label=""
                    selected-label="Sélectionné"
                    deselect-label=""
                    label="display"
                    track-by="id"
                    v-model="classe"
                    :show-no-options="false"
                    @input="getStudents('CL')"
                    @search-change="searchClasses"
                    class="mb-1"
                >
                    <template #noResult>
                        Aucune classe ne correspond à votre recherche.
                    </template>
                </multiselect>
            </b-col>
        </b-row>
        <b-row v-if="groups.length > 0">
            <b-col md="6">
                <b-form-group
                    label="Groupe"
                    label-cols="2"
                    label-class="font-weight-bold"
                >
                    <multiselect
                        :options="groups"
                        placeholder="Choisir un groupe"
                        select-label=""
                        selected-label="Sélectionné"
                        deselect-label="Ne plus filtrer"
                        :searchable="false"
                        v-model="studentGroup"
                        :show-no-options="false"
                        class="mb-1"
                    >
                        <template #noResult>
                            Aucune classe ne correspond à votre recherche.
                        </template>
                    </multiselect>
                </b-form-group>
            </b-col>
        </b-row>
        <b-row class="mt-2">
            <b-col cols="4">
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
                    Changements non-validés !
                </b-alert>
            </b-col>
        </b-row>
        <b-row class="mt-2">
            <b-col>
                <b-overlay :show="loadingStudent">
                    <b-list-group>
                        <add-absence-entry
                            v-for="s in filteredStudent"
                            :key="s.matricule"
                            :student="s"
                            @update="computeAlert"
                        />
                    </b-list-group>
                </b-overlay>
            </b-col>
        </b-row>
        <b-row
            v-if="students.length > 5"
            class="mt-2"
        >
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
    </div>
</template>

<script>
import Multiselect from "vue-multiselect";
import "vue-multiselect/dist/vue-multiselect.min.css";

import axios from "axios";
import Moment from "moment";

import { studentAbsenceTeacherStore } from "./stores/index.js";

import AddAbsenceEntry from "./add_absence_entry.vue";

const token = {xsrfCookieName: "csrftoken", xsrfHeaderName: "X-CSRFToken"};

export default {
    data: function () {
        return {
            periodOptions: [],
            givenCourseOptions: [],
            classesOptions: [],
            period: [],
            givenCourse: null,
            classe: null,
            students: [],
            showAlert: false,
            currentDate: Moment().format("YYYY-MM-DD"),
            loadingStudent: false,
            studentGroup: null,
            lastUpdate: null,
            store: studentAbsenceTeacherStore()
        };
    },
    computed: {
        filteredStudent: function () {
            if (!this.studentGroup) return this.students;

            const students = this.students.filter(s => s.group == this.studentGroup);
            this.store.resetChanges(students.map(s => s.matricule));
            return students;
        },
        groups: function () {
            const studentsWithGroup = this.students.filter(s => s.group);
            if (!studentsWithGroup) return [];

            return [...new Set(studentsWithGroup.map(s => s.group))];
        }
    },
    methods: {
        computeAlert: function () {
            this.showAlert = Object.keys(this.store.changes).length > 0;
        },
        searchClasses: function (query) {
            const data = {
                query: query,
                check_access: false,
                teachings: this.store.settings.teachings
            };
            axios.post("/annuaire/api/classes/", data, token)
                .then(resp => {
                    this.classesOptions = resp.data;
                });
        },
        getAbsence: function (students, selectBy) {
            const data = {
                params: {
                    period: this.period[0].id,
                    date_absence: this.currentDate,
                    page_size: 5000,
                }
            };
            if (selectBy === "GC") data.params.given_course = this.givenCourse.id;
            if (selectBy === "CL") data.params.student__classe = this.classe.id;
            axios.get("/student_absence_teacher/api/absence_teacher/", data, token)
                .then(resp => {
                    this.students = students.map(s => {
                        const savedAbsence = resp.data.results.find(r => r.student_id === s.matricule);
                        if (!savedAbsence) return s;

                        s.saved = savedAbsence;
                        return s;
                    });

                    // Save last data update.
                    resp.data.results.forEach(ab => {
                        if (!this.lastUpdate) {
                            this.lastUpdate = ab.datetime_update;
                        } else if (this.lastUpdate < ab.datetime_update) {
                            this.lastUpdate = ab.datetime_update;
                        }
                    });
                    this.loadingStudent = false;
                })
                .catch(err => {
                    alert(err);
                });
        },
        getStudents: function (selectBy, periodChange=false) {
            if (selectBy === "UND" || selectBy === undefined) {
                // If undefined, try givenCourse and then classe.
                selectBy = this.givenCourse ? "GC" : "CL";
            } else {
                this.studentGroup = null;
            }

            if (selectBy === "GC") {
                this.classe = null;
                if (!this.givenCourse || this.period.length === 0 || !this.currentDate) {
                    this.students = [];
                    this.showAlert = false;
                    this.store.resetChanges();
                    return;
                }

                if (periodChange) return;
                this.loadingStudent = true;
                this.students = [];
                axios.get(`/annuaire/api/student_given_course/${this.givenCourse.id}/`)
                    .then(resp => {
                        this.showAlert = false;
                        this.store.resetChanges();
                        this.getAbsence(resp.data, selectBy);
                    });
            } else if (selectBy === "CL") {
                this.givenCourse = null;
                if (!this.classe || this.period.length === 0 || !this.currentDate) {
                    this.students = [];
                    this.showAlert = false;
                    this.store.resetChanges();
                    return;
                }

                if (periodChange && this.period.length > 1) return;
                this.loadingStudent = true;
                this.students = [];
                const data = {params: {classe: this.classe.id}};
                axios.get("/annuaire/api/studentclasse", data)
                    .then(resp => {
                        this.store.resetChanges();
                        this.showAlert = false;
                        this.getAbsence(resp.data, selectBy);
                    });
            }
        },
        sendChanges: function () {
            const changes = this.store.changes;

            // Check if changes have been made in between.
            const data = {
                params: {
                    period: this.period[0].id,
                    date_absence: this.currentDate,
                    page_size: 5000,
                    datetime_update__gt: this.lastUpdate
                }
            };
            if (this.givenCourse) {
                data.params.given_course = this.givenCourse.id;
            } else {
                data.params.student__classe = this.classe.id;
            }
            axios.get("/student_absence_teacher/api/absence_teacher/", data, token)
                .then((resp) => {
                    if (resp.data.count > 0) {
                        const baseSentence = "Des changements ont eu lieu depuis le chargement initial des données. ";
                        const students = resp.data.results.map(ab => `${ab.student.last_name} ${ab.student.first_name}`).join(", ");
                        const changes = `Les élèves suivants ont été modifiés : ${students}. `;
                        const endSentence = "Tous les autres changements ont été sauvegardés.";
                        this.$bvModal.msgBoxOk(`${baseSentence} ${changes}${endSentence}`);
                    }

                    const promises = [];
                    for (let period in this.period) {
                        for (let matricule in changes) {
                            const change = changes[matricule];
                            if (resp.data.results.find(r => r.student.matricule === matricule)) {
                                continue;
                            }
                            const send = change.is_new ? axios.post : axios.put;
                            let url = "/student_absence_teacher/api/absence_teacher/";
                            if (!change.is_new) url += change.id + "/";
                            
                            const data = {
                                student_id: matricule,
                                period_id: this.period[period].id,
                                comment: change.comment,
                                status: change.status,
                                date_absence: this.currentDate
                            };
                            if (this.store.settings.select_student_by === "GC") data.given_course_id = this.givenCourse.id;
                            promises.push(send(url, data, token));
                        }
                    }
                    for (let matricule in changes) {
                        this.store.removeChange(matricule);
                    }
                    Promise.all(promises)
                        .then(resps => {
                            for (let r in resps) {
                                this.store.removeChange(resps[r].data.student_id);
                            }
                            resps.forEach(r => {
                                if (!this.lastUpdate) {
                                    this.lastUpdate = r.data.datetime_update;
                                } else if (this.lastUpdate < r.data.datetime_update) {
                                    this.lastUpdate = r.data.datetime_update;
                                }
                            });
                            this.$bvToast.toast("Les changements ont été sauvés.", {
                                variant: "success",
                                noCloseButton: true,
                            });
                            if (this.period.length === 1) {
                                this.getStudents();
                            } else {
                                this.students = [];
                                this.period = [];
                            }
                            
                            this.computeAlert();
                        })
                        .catch(err => {
                            alert(err);
                        });
                });
        },
    },
    mounted: function () {
        axios.get("/student_absence_teacher/api/period_teacher/")
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
