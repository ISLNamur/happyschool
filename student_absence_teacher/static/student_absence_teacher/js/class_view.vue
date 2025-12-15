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
        <BRow>
            <BCol class="text-right mb-1">
                <BButton
                    variant="primary"
                    @click="validateEducatorAbsences"
                >
                    Valider toutes les présences
                </BButton>
            </BCol>
        </BRow>
        <BRow>
            <BCol>
                <BOverlay :show="loading">
                    <BTable
                        id="classoverview"
                        :items="students"
                        :fields="fields"
                        class="text-center"
                        small
                    >
                        <template #head(absence)="">
                            <BRow>
                                <BCol
                                    v-for="p in teachersPeriod"
                                    :key="p.id"
                                    class="pr-1 pl-1"
                                >
                                    {{ p.start.slice(0, 5) }}
                                </BCol>
                            </BRow>
                            <BRow>
                                <BCol
                                    v-for="p in educatorsPeriod"
                                    :key="p.id"
                                >
                                    {{ p.name }}
                                </BCol>
                            </BRow>
                        </template>
                        <template #cell(studentName)="data">
                            <BLink
                                underline-variant="info"
                                underline-offset="3"
                                :to="`/overview/${date}/student_view/${data.item.matricule}/`"
                                @click="$emit('clearSearch')"
                            >
                                {{ data.value }}
                            </BLink>
                            <a :href="`/annuaire/#/person/student/${data.item.matricule}/`">
                                <IBiFileEarmarkRichtext />
                            </a>
                        </template>
                        <template #cell(absence)="data">
                            <overview-teacher-entry :absences="data.item.absence_teachers" />
                            <overview-educator-entry
                                :absences="data.item.absence_educators"
                                @update:model-value="updateEducatorAbsence($event, data.index)"
                            />
                        </template>
                        <template #cell(appel)="data">
                            <IBiTelephone
                                v-if="data.value"
                                v-b-tooltip.hover="data.value ? `${data.value.object} - ${data.value.motive.display}: ${data.value.commentaire}` : ''"
                            />
                        </template>
                        <template #cell(infirmery)="data">
                            <IBiPrescription2
                                v-if="data.value"
                                v-b-tooltip.hover="data.value ? `${data.value.motifs_admission} – ${data.value.remarques_sortie}` : ''"
                            />
                        </template>
                        <template #cell(isProcessed)="data">
                            <BFormCheckbox
                                :disabled="!data.item.absence_educators.some(a => a.status)"
                                v-model="students[data.index].isProcessed"
                                @update:model-value="updateIsProcessed($event, data.item)"
                            />
                        </template>
                    </BTable>
                </BOverlay>
            </BCol>
        </BRow>
    </div>
</template>

<script>
import axios from "axios";

import { displayStudent, extractDayOfWeek } from "@s:core/js/common/utilities.js";

import { studentAbsenceTeacherStore } from "./stores/index.js";

import OverviewTeacherEntry from "./overview_teacher_entry.vue";
import OverviewEducatorEntry from "./overview_educator_entry.vue";

const token = { xsrfCookieName: "csrftoken", xsrfHeaderName: "X-CSRFToken" };
export default {
    props: {
        classId: {
            type: String,
            default: "",
        },
        date: {
            type: String,
            default: "",
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
                    label: "",
                },
                {
                    key: "isProcessed",
                    label: "",
                },
            ],
            students: [],
            teachersPeriod: [],
            educatorsPeriod: [],
            classOptions: [],
            search: "",
            searchId: 0,
            store: studentAbsenceTeacherStore(),
        };
    },
    watch: {
        date: function () {
            this.updateStudentList();
        },
        classId: function () {
            this.updateStudentList();
        },
    },
    methods: {
        updateStudentList: function () {
            this.loading = true;
            this.getStudentsAbsences(this.classId, this.date);
        },
        updateIsProcessed: function (event, student) {
            student.absence_educators.filter(a => a.status !== null).forEach((a) => {
                axios.patch(`/student_absence_teacher/api/absence_educ/${a.id}/`, { is_processed: event }, token)
                    .then((resp) => {
                        student = resp.data;
                    });
            });
        },
        getSearchOptions: function (query) {
            // Ensure the last search is the first response.
            this.searchId += 1;
            let currentSearch = this.searchId;

            const token = { xsrfCookieName: "csrftoken", xsrfHeaderName: "X-CSRFToken" };
            let data = {
                query: query,
                teachings: this.store.settings.teachings,
                check_access: true,
            };
            axios.post("/annuaire/api/classes/", data, token)
                .then((response) => {
                    if (this.searchId !== currentSearch)
                        return;
                    this.classOptions = response.data;
                });
        },
        validateEducatorAbsences: function () {
            this.loading = true;
            const absencesData = this.educatorsPeriod.map((period, idx) => {
                // Consider "P" status if null.
                return this.students
                    .map(s => s.absence_educators[idx])
                    .filter(a => a.status === null)
                    .map((a) => {
                        a.status = "P";
                        return a;
                    });
            });

            axios.post("/student_absence_teacher/api/absence_educ/", absencesData.flat(), token)
                .then(() => {
                    document.location.reload();
                })
                .catch((err) => {
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
                axios.get(`/student_absence_teacher/api/absence_educ/?student__classe=${classId}&date_absence=${date}&page_size=500`),
            ];

            let additonalColumn = [];
            // eslint-disable-next-line no-undef
            if (menu.apps.find(a => a.app === "appels")) {
                additonalColumn.push({ column: "appel", position: promises.length });
                promises.push(
                    axios.get(`/appels/api/appel/?matricule__classe=${this.classId}&date_motif_start__gte=${this.date}&date_motif_end__lte=${this.date}`),
                );
            }
            // eslint-disable-next-line no-undef
            if (menu.apps.find(a => a.app === "infirmerie")) {
                additonalColumn.push({ column: "infirmery", position: promises.length });
                promises.push(
                    axios.get(`/infirmerie/api/passage/?matricule__classe=${this.classId}&datetime_arrive__gte=${this.date}&datetime_sortie__lte=${this.date} 23:59`),
                );
            }

            Promise.all(promises).then((resp) => {
                const currentDay = (new Date(date)).getDay();
                const teachersAbsences = resp[3].data.results;
                const educatorsAbsences = resp[4].data.results;
                this.teachersPeriod = resp[1].data.results
                    .filter(p => extractDayOfWeek(p.day_of_week).includes(currentDay));
                this.educatorsPeriod = resp[2].data.results
                    .filter(p => extractDayOfWeek(p.day_of_week).includes(currentDay));
                this.students = resp[0].data.map((s) => {
                    s.studentName = this.displayStudent(s);

                    s.absence_teachers = this.teachersPeriod.map((p) => {
                        const absence = teachersAbsences.find(a => a.period.id === p.id && a.student_id === s.matricule);
                        return absence ? absence : null;
                    });

                    s.absence_educators = this.educatorsPeriod.map((p) => {
                        const absence = educatorsAbsences.find(a => a.period === p.id && a.student_id === s.matricule);
                        return absence ? absence : { status: null, student_id: s.matricule, period: p.id, date_absence: date };
                    });
                    s.isProcessed = s.absence_educators.map(a => a.is_processed).every(p => p);
                    return s;
                });
                // Check if there are groups amongs students. If yes add group column.
                if (this.students.some(s => s.group)) {
                    if (this.fields.length === 2) {
                        this.fields.splice(1, 0, { key: "group", label: "Groupe" });
                    }
                }
                // Check if there are appels or infirmery passing.
                additonalColumn.forEach((aC) => {
                    this.fields.push(
                        {
                            key: aC.column,
                            label: "",
                        },
                    );

                    this.students.forEach((student) => {
                        student[aC.column] = resp[aC.position].data.results.find(a => a.matricule_id === student.matricule);
                    });
                });

                this.loading = false;
            });
        },
        displayStudent,
    },
    mounted: function () {
        this.getStudentsAbsences(this.classId, this.date);
    },
    components: {
        OverviewTeacherEntry,
        OverviewEducatorEntry,
    },
};
</script>

<style>
#classoverview table.BTable>thead>tr> :nth-child(2) {
    width: 75%;
}
</style>
