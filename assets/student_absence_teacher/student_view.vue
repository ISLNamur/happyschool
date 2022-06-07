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
                <b-input
                    :value="date"
                    type="date"
                    @change="moveToDate"
                    class="w-50"
                />
            </b-col>
            <b-btn @click="$router.go(-1)">
                Retour
            </b-btn>
        </b-row>
        <b-row class="mt-1">
            <b-col>
                <b-overlay :show="loading">
                    <b-table
                        id="classoverview"
                        :items="studentAsList"
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
                                @change="updateEducatorAbsence($event)"
                            />
                        </template>
                    </b-table>
                </b-overlay>
            </b-col>
        </b-row>
        <b-row>
            <b-col>
                <student-year-view
                    :student-id="parseInt(studentId)"
                    :current-date="date"
                />
            </b-col>
        </b-row>
    </div>
</template>

<script>
import axios from "axios";

import {displayStudent} from "../common/utilities.js";

import OverviewTeacherEntry from "./overview_teacher_entry.vue";
import OverviewEducatorEntry from "./overview_educator_entry.vue";
import StudentYearView from "./student_year_view.vue";


export default {
    props: {
        date: {
            type: String,
            default: ""
        },
        studentId: {
            type: String,
            default: -1
        }
    },
    data: function () {
        return {
            loading: false,
            student: null,
            teachersPeriod: [],
            educatorsPeriod: [],
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
        };
    },
    watch: {
        date: function () {
            document.location.reload();
        }
    },
    computed: {
        studentAsList: function () {
            if (this.student) return [this.student];

            return [];
        }
    },
    methods: {
        displayStudent,
        moveToDate: function(newDate) {
            this.$router.push(`/student_view/${this.studentId}/${newDate}/`, () => {
                document.location.reload();
            });
        },
        updateEducatorAbsence: function (payload) {
            const data = payload[0];
            const periodIndex = payload[1];
            this.student.absence_educators[periodIndex] = data;
        },
        getStudentAbsences: function () {
            const promises = [
                axios.get(`/annuaire/api/student/${this.studentId}/`),
                axios.get("/student_absence_teacher/api/period/"),
                axios.get("/student_absence/api/period/"),
                axios.get(`/student_absence_teacher/api/absence/?student__matricule=${this.studentId}&date_absence=${this.date}&page_size=500`),
                axios.get(`/student_absence/api/student_absence/?student__matricule=${this.studentId}&date_absence=${this.date}&page_size=500`)
            ];
            Promise.all(promises).then(resp => {
                const teachersAbsences = resp[3].data.results;
                const educatorsAbsences = resp[4].data.results;
                this.teachersPeriod = resp[1].data.results;
                this.educatorsPeriod = resp[2].data.results;
                this.student = resp[0].data;
                this.student.studentName = this.displayStudent(this.student);
                this.student.absence_teachers = this.teachersPeriod.map(p => {
                    const absence = teachersAbsences.find(a => a.period.id === p.id);
                    return absence ? absence : null;
                });
                this.student.absence_educators = this.educatorsPeriod.map(p => {
                    const absence = educatorsAbsences.find(a => a.period === p.id);
                    return absence ? absence : {is_absent: null, student_id: this.student.matricule, period: p.id, date_absence: this.date};
                });

            });
        },
    },
    mounted: function () {
        this.getStudentAbsences();
    },
    components: {
        OverviewTeacherEntry,
        OverviewEducatorEntry,
        StudentYearView,
    }
};
</script>
