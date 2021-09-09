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
            <b-col>
                Date : {{ date }}
            </b-col>
            <b-col class="text-right mb-1">
                <b-btn
                    variant="primary"
                    @click="validateEducatorAbsences"
                >
                    Valider la classe
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

import {displayStudent} from "../common/utilities.js";
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
        }
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
        };
    },
    methods: {
        validateEducatorAbsences: function () {
            this.loading = true;
            const absencesProm = this.educatorsPeriod.map((period, idx) => {
                const absences = this.students
                    .map(s => s.absence_educators[idx])
                    .filter(a => a.is_absent === null)
                    .map(a => {
                        a.is_absent = false;
                        return a;
                    });
                return axios.post("/student_absence/api/student_absence/", absences, token);
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
        getStudentsAbsences: function () {
            const promises = [
                axios.get(`/annuaire/api/studentclasse/?classe=${this.classId}`),
                axios.get("/student_absence_teacher/api/period/"),
                axios.get("/student_absence/api/period/"),
                axios.get(`/student_absence_teacher/api/absence/?student__classe=${this.classId}&date_absence=${this.date}&page_size=500`),
                axios.get(`/student_absence/api/student_absence/?student__classe=${this.classId}&date_absence=${this.date}&page_size=500`)
            ];
            Promise.all(promises).then(resp => {
                const teachersAbsences = resp[3].data.results;
                const educatorsAbsences = resp[4].data.results;
                this.students = resp[0].data.map(s => {
                    s.studentName = this.displayStudent(s);
                    this.teachersPeriod = resp[1].data.results;
                    this.educatorsPeriod = resp[2].data.results;
                    s.absence_teachers = this.teachersPeriod.map(p => {
                        const absence = teachersAbsences.find(a => a.period.id === p.id && a.student_id === s.matricule);
                        return absence ? absence.status : null;
                    });
                    s.absence_educators = this.educatorsPeriod.map(p => {
                        const absence = educatorsAbsences.find(a => a.period === p.id && a.student_id === s.matricule);
                        return absence ? absence : {is_absent: null, student_id: s.matricule, period: p.id, date_absence: this.date};
                    });
                    return s;
                });
            });
        },
        displayStudent
    },
    mounted: function () {
        this.getStudentsAbsences();
    },
    components: {
        OverviewTeacherEntry,
        OverviewEducatorEntry,
    }
};
</script>

<style>
    #classoverview table.b-table > thead > tr > :nth-child(2) {
        width: 75%;
    }
</style>
