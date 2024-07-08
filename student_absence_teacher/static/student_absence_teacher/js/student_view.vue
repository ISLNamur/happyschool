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
        <b-row class="mt-1">
            <b-col>
                <b-overlay :show="loading">
                    <b-table
                        id="classoverview"
                        :items="studentAsList"
                        :fields="fields"
                        class="text-center"
                    >
                        <template
                            v-if="date !== 'null'"
                            #head(absence)=""
                        >
                            <b-row>
                                <b-col
                                    v-for="p in teachersPeriod"
                                    :key="p.id"
                                    class="pr-1 pl-1"
                                >
                                    {{ p.start.slice(0, 5) }}
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
                            {{ data.value }}
                            <a :href="`/annuaire/#/person/student/${data.item.matricule}/`">
                                <b-icon icon="file-earmark-richtext" />
                            </a>
                        </template>
                        <template
                            v-if="date !== 'null'"
                            #cell(absence)="data"
                        >
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
                <b-card no-body>
                    <template
                        #header
                    >
                        <div class="d-flex justify-content-between align-items-center">
                            <strong>Absences</strong>
                        </div>
                    </template>
                    <b-list-group>
                        <b-list-group-item class="d-flex justify-content-between align-items-center">
                            Absences en attentes de justificatifs
                            <b-badge :variant="pendingAbsences > 0 ? 'warning' : ''">
                                {{ pendingAbsences }}
                            </b-badge>
                        </b-list-group-item>

                        <b-list-group-item
                            variant="secondary"
                        >
                            <strong>Absences motivées:</strong>
                        </b-list-group-item>
                        <b-list-group-item
                            v-for="justCount in justifiedAbsences"
                            :key="justCount.justificationmodel__motive__short_name"
                            class="d-flex justify-content-between align-items-center"
                        >
                            <span>
                                <strong>{{ justCount.justificationmodel__motive__short_name }}</strong>:
                                {{ justCount.justificationmodel__motive__name.slice(0, 50) }}
                                <span v-if="justCount.justificationmodel__motive__name.length > 50">…</span>
                            </span>
                            <b-badge
                                :id="`just-count-badge-${justCount.justificationmodel__motive__short_name}`"
                                :variant="justCount.justificationmodel__motive__count > justCount.justificationmodel__motive__admissible_up_to ? 'danger' : ''"
                            >
                                {{ justCount.justificationmodel__motive__count }}
                            </b-badge>
                            <b-tooltip
                                v-if="justCount.justificationmodel__motive__count > justCount.justificationmodel__motive__admissible_up_to"
                                :target="`just-count-badge-${justCount.justificationmodel__motive__short_name}`"
                                triggers="hover"
                            >
                                Max. {{ justCount.justificationmodel__motive__admissible_up_to }}
                            </b-tooltip>
                        </b-list-group-item>
                        <b-list-group-item
                            class="d-flex justify-content-between align-items-center"
                        >
                            <strong>Total justifiées / motivées:</strong>
                            <span>
                                <b-badge variant="primary">
                                    {{ totalAdmissibleCount }}
                                </b-badge>
                                /
                                <b-badge variant="primary">
                                    {{ totalJustCount }}
                                </b-badge>
                            </span>
                        </b-list-group-item>
                        <b-list-group-item
                            variant="danger"
                        >
                            <strong>Absences non justifiées:</strong>
                        </b-list-group-item>
                        <b-list-group-item
                            v-for="justCount in unjustifiedAbsences"
                            :key="justCount.justificationmodel__motive__short_name"
                            class="d-flex justify-content-between align-items-center"
                        >
                            <span>
                                <strong>{{ justCount.justificationmodel__motive__short_name }}</strong>:
                                {{ justCount.justificationmodel__motive__name.slice(0, 50) }}
                            </span>
                            <b-badge>
                                {{ justCount.justificationmodel__motive__count }}
                            </b-badge>
                        </b-list-group-item>
                        <b-list-group-item
                            class="d-flex justify-content-between align-items-center"
                        >
                            <strong>Total :</strong>
                            <b-badge variant="danger">
                                {{ totalUnjustCount }}
                            </b-badge>
                        </b-list-group-item>
                    </b-list-group>
                </b-card>
            </b-col>
            <b-col>
                <b-card
                    no-body
                    class="scrollable"
                >
                    <template
                        #header
                    >
                        <div class="d-flex justify-content-between align-items-center">
                            <strong>Justificatif</strong>
                            <b-badge variant="primary">
                                {{ justifications.length }}
                            </b-badge>
                        </div>
                    </template>
                    <b-list-group flush>
                        <b-list-group-item
                            v-for="just in justifications"
                            :key="just.id"
                        >
                            <div class="d-flex w-100 justify-content-between">
                                <span>
                                    <strong :id="`motive-name-${just.id}`">{{ just.motive.short_name }}</strong> :
                                    {{ just.date_just_start }} ({{ this.educatorsPeriod[just.half_day_start].name }})
                                    – {{ just.date_just_end }} ({{ this.educatorsPeriod[just.half_day_end].name }}) 
                                    <span>
                                        <b-icon
                                            v-if="just.comment"
                                            :id="`comment-${just.id}`"
                                            icon="chat-text"
                                        />
                                        <b-tooltip
                                            :target="`comment-${just.id}`"
                                            triggers="hover"
                                        >
                                            {{ just.comment }}
                                        </b-tooltip>
                                    </span>
                                    <b-tooltip
                                        :target="`motive-name-${just.id}`"
                                        triggers="hover"
                                    >
                                        {{ just.motive.name }}
                                    </b-tooltip>
                                </span>
                                <span>
                                    <b-btn
                                        :to="`/justification/${just.id}/`"
                                        variant="outline-success"
                                        size="sm"
                                    >
                                        <b-icon icon="pencil-square" />
                                    </b-btn>
                                </span>
                            </div>
                        </b-list-group-item>
                    </b-list-group>
                </b-card>
            </b-col>
        </b-row>
        <b-row class="mt-2">
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

import { displayStudent } from "@s:core/js/common/utilities.js";

import { studentAbsenceTeacherStore } from "./stores/index.js";

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
            pendingAbsences: 0,
            justifiedAbsences: [],
            unjustifiedAbsences: [],
            justifications: [],
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
            store: studentAbsenceTeacherStore(),
        };
    },
    watch: {
        date: function () {
            this.getStudentAbsences();
        }
    },
    computed: {
        studentAsList: function () {
            if (this.student) return [this.student];

            return [];
        },
        totalJustCount: function () {
            return this.justifiedAbsences.reduce((p, c) => p + c.justificationmodel__motive__count, 0);
        },
        totalAdmissibleCount: function () {
            return this.justifiedAbsences.reduce((p, c) => {
                if (c.justificationmodel__motive__count > c.justificationmodel__motive__admissible_up_to) {
                    return p + c.justificationmodel__motive__admissible_up_to;
                }
                return p + c.justificationmodel__motive__count;
            }, 0);
        },
        totalUnjustCount: function () {
            return this.unjustifiedAbsences.reduce((p, c) => p + c.justificationmodel__motive__count, 0);
        }
    },
    methods: {
        displayStudent,
        updateEducatorAbsence: function (payload) {
            console.log("coucou");
            const data = payload[0];
            const periodIndex = payload[1];
            this.student.absence_educators[periodIndex] = data;
        },
        getStudentAbsences: function () {
            const promises = [
                axios.get(`/annuaire/api/student/${this.studentId}/`),
                axios.get("/student_absence_teacher/api/period_teacher/"),
                axios.get("/student_absence_teacher/api/period_educ/"),
                // eslint-disable-next-line no-undef
                axios.get(`/student_absence_teacher/api/justification/?student__matricule=${this.studentId}&ordering=date_just_start&scholar_year=${current_scholar_year}-${current_scholar_year + 1}`),
                axios.get("/student_absence_teacher/api/just_motive/"),
            ];
            if (this.date !== "null") {
                promises.push(axios.get(`/student_absence_teacher/api/absence_teacher/?student__matricule=${this.studentId}&date_absence=${this.date}&page_size=500`));
                promises.push(axios.get(`/student_absence_teacher/api/absence_educ/?student__matricule=${this.studentId}&date_absence=${this.date}&page_size=500`));
            }
            Promise.all(promises).then(resp => {
                this.teachersPeriod = resp[1].data.results;
                this.educatorsPeriod = resp[2].data.results;
                this.student = resp[0].data;
                this.student.studentName = this.displayStudent(this.student);
                this.justifications = resp[3].data.results
                    .map(j => {
                        j.motive = resp[4].data.results.find(m => j.motive === m.id);
                        return j;
                    });

                if (promises.length === 5) {
                    return;
                }
                const teachersAbsences = resp[5].data.results;
                const educatorsAbsences = resp[6].data.results;
                this.student.absence_teachers = this.teachersPeriod.map(p => {
                    const absence = teachersAbsences.find(a => a.period.id === p.id);
                    return absence ? absence : null;
                });
                this.student.absence_educators = this.educatorsPeriod.map(p => {
                    const absence = educatorsAbsences.find(a => a.period === p.id);
                    return absence ? absence : { status: null, student_id: this.student.matricule, period: p.id, date_absence: this.date };
                });
                
            });

            axios.get(`/student_absence_teacher/api/count_no_justification/${this.studentId}/`)
                .then((resp) => {
                    this.pendingAbsences = resp.data.count;
                });
            axios.get(`/student_absence_teacher/api/count_justification/${this.studentId}/`)
                .then((resp) => {
                    this.justifiedAbsences = resp.data.justified;
                    this.unjustifiedAbsences = resp.data.unjustified;
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

<style>
.scrollable {
    height:400px;
    overflow-y: scroll;
}
</style>
