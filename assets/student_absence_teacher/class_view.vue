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
            <b-col md="4">
                <b-input
                    :value="date"
                    type="date"
                    @change="moveToDate"
                />
            </b-col>
            <b-col md="4">
                <b-form-group>
                    <multiselect
                        :show-no-options="false"
                        :internal-search="false"
                        :options="classOptions"
                        @search-change="getSearchOptions"
                        placeholder="Rechercher classe"
                        select-label=""
                        selected-label="Sélectionné"
                        deselect-label=""
                        label="display"
                        track-by="id"
                        :v-model="search"
                        @select="moveToClass"
                    >
                        <template #noResult>
                            Aucune classe trouvée.
                        </template>
                        <template #noOptions />
                    </multiselect>
                </b-form-group>
            </b-col>
            <b-col class="text-right mb-1">
                <b-btn
                    variant="primary"
                    @click="validateEducatorAbsences"
                >
                    Valider toutes les présences
                </b-btn>
            </b-col>
        </b-row>
        <b-row>
            <b-col>
                <b-overlay :show="loading">
                    <b-table
                        id="classoverview"
                        :items="students"
                        :fields="fields"
                        class="text-center"
                        small
                    >
                        <template #head(absence)="">
                            <b-row>
                                <b-col
                                    v-for="p in teachersPeriod"
                                    :key="p.id"
                                    class="pr-1 pl-1"
                                >
                                    {{ p.start.slice(0,5) }}
                                </b-col>
                            </b-row>
                            <b-row>
                                <b-col
                                    v-for="p in educatorsPeriod"
                                    :key="p.id"
                                >
                                    {{ p.name }}
                                </b-col>
                            </b-row>
                        </template>
                        <template #cell(studentName)="data">
                            <a :href="`#/student_view/${data.item.matricule}/${date}/`">{{ data.value }}</a>
                            <a :href="`/annuaire/#/person/student/${data.item.matricule}/`">
                                <b-icon icon="file-earmark-richtext" />
                            </a>
                        </template>
                        <template #cell(absence)="data">
                            <overview-teacher-entry :absences="data.item.absence_teachers" />
                            <overview-educator-entry
                                :absences="data.item.absence_educators"
                                @change="updateEducatorAbsence($event, data.index)"
                            />
                        </template>
                    </b-table>
                </b-overlay>
            </b-col>
        </b-row>
    </div>
</template>

<script>
import axios from "axios";
import Multiselect from "vue-multiselect";

import {displayStudent, extractDayOfWeek} from "../common/utilities.js";

import { studentAbsenceTeacherStore } from "./stores/index.js";

import OverviewTeacherEntry from "./overview_teacher_entry.vue";
import OverviewEducatorEntry from "./overview_educator_entry.vue";


const token = {xsrfCookieName: "csrftoken", xsrfHeaderName: "X-CSRFToken"};
export default {
    props: {
        classId: {
            type: String,
            default: "",
        },
        date: {
            type: String,
            default: ""
        },
    },
    data: function () {
        return {
            loading: false,
            fields: [
                {
                    key: "studentName",
                    label: "Nom",
                },
                {
                    key: "absence",
                    label: ""
                }
            ],
            students: [],
            teachersPeriod: [],
            educatorsPeriod: [],
            classOptions: [],
            search: "",
            searchId: 0,
            store: studentAbsenceTeacherStore()
        };
    },
    methods: {
        moveToDate: function(newDate) {
            this.$router.push(`/class_view/${this.classId}/${newDate}/`, () => {
                this.loading = true;
                this.getStudentsAbsences(this.classId, newDate);
            });
        },
        moveToClass: function(newClass) {
            this.$router.push(`/class_view/${newClass.id}/${this.date}/`, () => {
                this.loading = true;
                this.getStudentsAbsences(newClass.id, this.date);
            });
        },
        getSearchOptions: function (query) {
            // Ensure the last search is the first response.
            this.searchId += 1;
            let currentSearch = this.searchId;

            const token = { xsrfCookieName: "csrftoken", xsrfHeaderName: "X-CSRFToken"};
            let data = {
                query: query,
                teachings: this.store.settings.teachings,
                check_access: true
            };
            axios.post("/annuaire/api/classes/", data, token)
                .then(response => {
                    if (this.searchId !== currentSearch)
                        return;
                    this.classOptions = response.data;
                });
        },
        validateEducatorAbsences: function () {
            this.loading = true;
            const absencesProm = this.educatorsPeriod.map((period, idx) => {
                // Consider "P" status if null.
                const absences = this.students
                    .map(s => s.absence_educators[idx])
                    .filter(a => a.status === null)
                    .map(a => {
                        a.status = "P";
                        return a;
                    });
                return axios.post("/student_absence_teacher/api/absence_educ/", absences, token);
            });
            
            Promise.all(absencesProm)
                .then(() => {
                    document.location.reload();
                })
                .catch(err => {
                    console.log(err);
                    this.loading = false;
                });
        },
        updateEducatorAbsence: function (payload, studentIndex) {
            const data = payload[0];
            const periodIndex = payload[1];
            this.students[studentIndex].absence_educators[periodIndex] = data;
        },
        getStudentsAbsences: function (classId, date) {
            this.students = [];
            const promises = [
                axios.get(`/annuaire/api/studentclasse/?classe=${classId}`),
                axios.get("/student_absence_teacher/api/period_teacher/"),
                axios.get("/student_absence_teacher/api/period_educ/"),
                axios.get(`/student_absence_teacher/api/absence_teacher/?student__classe=${classId}&date_absence=${date}&page_size=500`),
                axios.get(`/student_absence_teacher/api/absence_educ/?student__classe=${classId}&date_absence=${date}&page_size=500`)
            ];
            Promise.all(promises).then(resp => {
                const currentDay = (new Date(date)).getDay();
                const teachersAbsences = resp[3].data.results;
                const educatorsAbsences = resp[4].data.results;
                this.teachersPeriod = resp[1].data.results
                    .filter(p => extractDayOfWeek(p.day_of_week).includes(currentDay));
                this.educatorsPeriod = resp[2].data.results
                    .filter(p => extractDayOfWeek(p.day_of_week).includes(currentDay));
                this.students = resp[0].data.map(s => {
                    s.studentName = this.displayStudent(s);

                    s.absence_teachers = this.teachersPeriod.map(p => {
                        const absence = teachersAbsences.find(a => a.period.id === p.id && a.student_id === s.matricule);
                        return absence ? absence : null;
                    });

                    s.absence_educators = this.educatorsPeriod.map(p => {
                        const absence = educatorsAbsences.find(a => a.period === p.id && a.student_id === s.matricule);
                        return absence ? absence : {status: null, student_id: s.matricule, period: p.id, date_absence: date};
                    });
                    return s;
                });
                // Check if there are groups amongs students. If yes add group column.
                if (this.students.some(s => s.group)) {
                    if (this.fields.length === 2) {
                        this.fields.splice(1, 0, { key: "group", label: "Groupe"});
                    }
                }
                this.loading = false;
            });
        },
        displayStudent
    },
    mounted: function () {
        this.getStudentsAbsences(this.classId, this.date);
    },
    components: {
        OverviewTeacherEntry,
        OverviewEducatorEntry,
        Multiselect
    }
};
</script>

<style>
    #classoverview table.b-table > thead > tr > :nth-child(2) {
        width: 75%;
    }
</style>
