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
        <b-card
            no-body
            :class="studentAbsenceClass"
        >
            <b-row class="m-1">
                <b-col>
                    <strong>{{ absence.date_absence }}</strong>:
                    <a :href="`/annuaire/#/person/student/${absence.student.matricule}/`">
                        {{ displayStudent(absence.student) }}
                    </a>
                    <b-btn
                        variant="link"
                        size="sm"
                        @click="filterStudent"
                    >
                        <b-icon icon="funnel" />
                    </b-btn>
                    <div>
                        <strong>{{ status }}</strong>
                        {{ absence.period.name }}
                        {{ useCourse ? `(${absence.given_course.display})` : "" }}
                        <p>{{ absence.comment }}</p>
                    </div>
                </b-col>
                <b-col
                    v-if="studentAbsenceComparison !== 'match'"
                    cols="12"
                    sm="6"
                    lg="6"
                    class="text-right"
                >
                    <p v-if="studentAbsenceComparison === 'mismatch'">
                        La présence chez les éducateurs est <strong>différente</strong>.
                    </p>
                    <p v-if="studentAbsenceComparison === 'notset'">
                        Aucune présence chez les éducateurs.
                    </p>
                    <b-overlay :show="updating">
                        <b-btn
                            @click="pushStudentAbs()"
                            class="m-1"
                        >
                            Mettre à jour l'entrée de l'éducateur
                        </b-btn>
                    </b-overlay>
                    <div v-if="studentAbsenceComparison === 'mismatch'">
                        <b-overlay :show="updating">
                            <b-btn
                                @click="pullStudentAbs()"
                                class="m-1"
                            >
                                Mettre à jour l'entrée du prof
                            </b-btn>
                        </b-overlay>
                    </div>
                </b-col>
            </b-row>
        </b-card>
    </div>
</template>

<script>
import axios from "axios";

import { studentAbsenceTeacherStore } from "./stores/index.js";

import { displayStudent } from "@s:core/js/common/utilities.js";

const absenceLabel = {
    "presence": "Présence",
    "absence": "Absence",
    "lateness": "Retard",
    "excluded": "Exclus",
    "internship": "Stage",
};
const token = { xsrfCookieName: "csrftoken", xsrfHeaderName: "X-CSRFToken" };

export default {
    props: {
        "absence": {
            type: Object,
            default: () => { }
        }
    },
    data: function () {
        return {
            studentAbsenceState: null,
            relatedStudentAbsence: [],
            updating: false,
            store: studentAbsenceTeacherStore(),
        };
    },
    computed: {
        useCourse: function () {
            return this.store.settings.select_student_by === "GC";
        },
        status: function () {
            return absenceLabel[this.absence.status];
        },
        studentAbsenceComparison: function () {
            if (!this.studentAbsenceState) return "notset";
            if (this.studentAbsenceState == this.absence.status) return "match";
            if (this.absence.status == "lateness" && this.studentAbsenceState == "presence") return "match";
            return "mismatch";
        },
        studentAbsenceClass: function () {
            switch (this.studentAbsenceComparison) {
            case "notset":
                return "bg-warning";
            case "match":
                return "bg-success";
            case "mismatch":
                return "bg-danger";
            }
            return "";
        },
    },
    methods: {
        filterStudent: function () {
            this.$emit("filterStudent", this.absence.student_id);
        },
        displayStudent,
        checkStudentAbsence: function () {
            axios.get(`/student_absence_teacher/api/absence_educ/?student__matricule=${this.absence.student.matricule}&date_absence=${this.absence.date_absence}&period__start__lt=${this.absence.period.end}&period__end__gt=${this.absence.period.start}`)
                .then(resp => {
                    if (resp.data.results.length > 0) {
                        this.studentAbsenceState = resp.data.results.filter(sA => sA.is_absent).length > 0 ? "absence" : "presence";
                        this.relatedStudentAbsence = resp.data.results;
                    }
                    this.updating = false;
                });
        },
        pushStudentAbs: function () {
            this.updating = true;
            if (!this.studentAbsenceState) {
                axios.get(`/student_absence_teacher/api/period_educ/?start__lt=${this.absence.period.end}&end__gt=${this.absence.period.start}`)
                    .then(resp => {
                        const data = resp.data.results.map(p => {
                            return {
                                student_id: this.absence.student.matricule,
                                date_absence: this.absence.date_absence,
                                period: p.id,
                                is_absent: this.absence.status == "absence"
                            };
                        });
                        axios.post("/student_absence_teacher/api/absence_educ/", data, token)
                            .then(() => {
                                this.checkStudentAbsence();
                            });
                    });
            } else {
                const studentAbsencePromise = this.relatedStudentAbsence.map(studAbs => {
                    const data = {
                        student_id: this.absence.student.matricule,
                        date_absence: this.absence.date_absence,
                        period: studAbs.period,
                        is_absent: this.absence.status == "absence"
                    };
                    return axios.put(`/student_absence_teacher/api/absence_educ/${studAbs.id}/`, data, token);
                });
                Promise.all(studentAbsencePromise)
                    .then(() => {
                        this.checkStudentAbsence();
                    });
            }
        },
        pullStudentAbs: function () {
            this.updating = true;
            const data = {
                status: this.absence.status === "presence" || this.absence.status === "lateness" ? "absence" : "presence"
            };
            axios.patch(`/student_absence_teacher/api/absence_teacher/${this.absence.id}/`, data, token)
                .then(() => {
                    this.$emit("update");
                    this.updating = false;
                });
        }
    },
    mounted: function () {
        this.checkStudentAbsence();
    }
};
</script>
