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
    <BRow>
        <BCol>
            <BOverlay :show="loading">
                <BTable
                    hover
                    bordered
                    :items="absence_count"
                    :fields="fields"
                    :filter="filter"
                    :filterable="['classe']"
                >
                    <template #head(classe)="">
                        <div class="d-flex justify-content-between">
                            <BButton
                                v-b-toggle.massive-attendance
                                variant="outline-primary"
                            >
                                <IBiClipboardCheck />
                            </BButton>

                            <BButton
                                v-b-toggle.other-options
                                variant="primary"
                                class="ms-1"
                            >
                                <IBiGear />
                            </BButton>

                            <BInputGroup class="ms-1">
                                <BFormInput
                                    v-model="filter"
                                    type="search"
                                    id="filterInput"
                                    placeholder=""
                                />
                                <template #prepend>
                                    <BInputGroupText>
                                        <IBiFunnel />
                                    </BInputGroupText>
                                </template>
                            </BInputGroup>
                        </div>
                    </template>
                    <template #cell(classe)="data">
                        <BLink
                            underline-offset="3"
                            underline-variant="info"
                            :to="`/overview/${date}/class_view/${data.item.classe__id}/`"
                        >
                            {{ data.value }}
                        </BLink>
                    </template>
                    <template #cell()="data">
                        <span v-if="data.value.teacher_count >= 0">
                            {{ data.value.teacher_count }}
                        </span>
                        <span v-else>-</span>
                        <span v-if="'not_teacher_count' in data.value">
                            /
                            <span v-if="data.value.not_teacher_count >= 0">
                                {{ data.value.not_teacher_count }}
                            </span>
                            <span v-else>-</span>
                        </span>
                    </template>
                </BTable>
            </BOverlay>
        </BCol>
    </BRow>
    <BModal
        id="massive-attendance"
        ref="massive-attendance"
    >
        <BOverlay :show="massiveAttendanceLoading">
            <p>Les élèves des classes suivantes seront mis comme <strong>«présents»</strong>. Les élèves qui sont déjà mis comme «absents» ne seront pas affectés.</p>
            <p>
                {{ absence_count.filter(a => a.classe.includes(filter)).map(a => a.classe).join(", ") }}
            </p>
            <div class="text-center">
                <BButton
                    variant="success"
                    @click="massiveAttendance"
                >
                    <IBiClipboardCheck />
                    Marquer présent
                </BButton>
            </div>
        </BOverlay>
        <div class="mt-2">
            <BProgress :value="massiveAttendanceProgress * 100" />
        </div>
        <template #footer>
            <span />
        </template>
    </BModal>
    <BModal
        id="other-options"
        title="Options de visualisation"
        ok-only
        right
        shadow
    >
        <BFormGroup
            label="Vue horaire"
            v-slot="{ ariaDescribedby }"
            class="ml-1"
        >
            <BFormRadioGroup
                id="point-of-view-radio"
                v-model="pointOfView"
                :options="optionsPointOfView"
                :aria-describedby="ariaDescribedby"
                button-variant="outline-primary"
                name="point-of-view-radio"
                @update:model-value="get_absence_count()"
                buttons
            />
        </BFormGroup>
        <BFormGroup
            label="Liste des classes"
            v-slot="{ ariaDescribedby }"
            class="ml-1"
        >
            <BFormRadioGroup
                id="class-list-type-radio"
                v-model="classListType"
                :options="optionsClassListType"
                :aria-describedby="ariaDescribedby"
                button-variant="outline-primary"
                name="class-list-type-radio"
                @update:model-value="get_absence_count()"
                buttons
            />
        </BFormGroup>
        <BFormGroup
            v-if="isProecoActivated"
            label="Export vers ProEco"
            class="ml-1"
        >
            <BDropdown
                text="Export"
                variant="outline-secondary"
            >
                <BDropdownItem
                    v-for="p in educatorPeriods"
                    :key="p.id"
                    :href="`/student_absence_teacher/api/export_selection/?page_size=2000&date_absence=${date}&period__name=${p.name}&status=A${exportOwnClasses}`"
                >
                    {{ p.name }}
                </BDropdownItem>
                <BDropdownItem
                    :href="`/student_absence_teacher/api/export_selection/?page_size=2000&date_absence=${date}&status=A${exportOwnClasses}`"
                >
                    Toute la journée
                </BDropdownItem>
            </BDropdown>
        </BFormGroup>
    </BModal>
</template>

<script>
import axios from "axios";

import Moment from "moment";
import "moment/dist/locale/fr";
Moment.locale("fr");

import { extractDayOfWeek } from "@s:core/js/common/utilities.js";

import { studentAbsenceTeacherStore } from "./stores/index.js";

const token = { xsrfCookieName: "csrftoken", xsrfHeaderName: "X-CSRFToken" };

export default {
    props: {
        date: {
            type: String,
            default: () => Moment().format("YYYY-MM-DD"),
        },
    },
    data: function () {
        return {
            pointOfView: "teacher",
            optionsPointOfView: [
                { text: "Prof.", value: "teacher" },
                { text: "Éduc.", value: "educator" },
            ],
            classListType: "ownclass",
            optionsClassListType: [
                { text: "Ses classes", value: "ownclass" },
                { text: "Toutes", value: "allclass" },
            ],
            absence_count: [],
            fields: [
            ],
            educatorPeriods: [],
            filter: "",
            loading: true,
            massiveAttendanceLoading: false,
            massiveAttendanceProgress: 0,
            searchOptions: [],
            search: "",
            searchId: -1,
            store: studentAbsenceTeacherStore(),
        };
    },
    computed: {
        isProecoActivated: function () {
            // eslint-disable-next-line no-undef
            return proeco;
        },
        exportOwnClasses: function () {
            return this.classListType === "ownclass" ? "&activate_own_classes=true" : "";
        },
    },
    watch: {
        date: function () {
            this.get_absence_count();
        },
    },
    methods: {
        /** Updates the massive attendance information of multiple students in multiple classes.
         *
         * @async
         * @return {void}
         */
        async massiveAttendance() {
            this.massiveAttendanceLoading = true;
            const classes = this.absence_count.filter(a => a.classe.includes(this.filter)).map(a => a.classe__id);

            if (classes.length === 0) {
                this.$refs["massive-attendance"].hide();
                this.massiveAttendanceLoading = false;
                return;
            }

            const tasks = classes.map((c) => {
                return p => axios.post(
                    "/student_absence_teacher/api/massive_attendance/",
                    { class_id: c, period_id: p, date: this.date },
                    token);
            });

            const totalRequests = this.educatorPeriods.length * classes.length;
            let processed = 0;
            for (const task in tasks) {
                for (const p in this.educatorPeriods) {
                    await tasks[task](this.educatorPeriods[p].id);
                    processed++;
                    this.massiveAttendanceProgress = processed / totalRequests;
                }
            }

            this.$refs["massive-attendance"].hide();
            this.massiveAttendanceLoading = false;
            this.massiveAttendanceProgress = 0;
            this.get_absence_count();
        },
        /**
        * Navigates to a new page for the given date.
        * @param {Date} evt The date object representing the date to navigate to.
        */
        changeDate: function (evt) {
            this.$router.push(`/overview/${evt}/`);
        },
        /**
         * Fetches a list of periods and their absence counts from the server
         * and highlights period rows with mismatching teacher/educator attendance.
         */
        get_absence_count: function () {
            this.loading = true;
            this.absence_count = [];
            this.getPeriods();
            axios.get(`/student_absence_teacher/api/count_absence/${this.date}/${this.pointOfView}/${this.classListType}/`)
                .then((resp) => {
                    this.absence_count = JSON.parse(resp.data).map((row) => {
                        const periods = Object.entries(row).filter(c => c[0].startsWith("period"));
                        const emptyPeriods = periods.filter(p => p[1]["teacher_count"] < 0);
                        row._cellVariants = emptyPeriods.reduce((acc, v) => {
                            acc[v[0]] = "warning";
                            return acc;
                        }, {});
                        if (periods.length > 0 && "not_teacher_count" in periods[0][1]) {
                            const mismatchPeriods = periods.filter((p) => {
                                if (p[1]["not_teacher_count"] < 0 || p[1]["teacher_count"] < 0) {
                                    return false;
                                }
                                if (p[1]["not_teacher_count"] != p[1]["teacher_count"]) {
                                    return true;
                                }
                                return false;
                            });
                            mismatchPeriods.forEach((p) => {
                                row._cellVariants[p[0]] = "danger";
                            });
                        }
                        return row;
                    });
                    this.loading = false;
                });
        },
        getPeriods: function () {
            this.fields = [{ key: "classe" }];
            const currentDay = (new Date(this.date)).getDay();

            if (this.pointOfView === "teacher") {
                axios.get("/student_absence_teacher/api/period_teacher/")
                    .then((resp) => {
                        this.fields = this.fields.concat(
                            resp.data.results
                                .filter(p => extractDayOfWeek(p.day_of_week).includes(currentDay))
                                .map((p) => {
                                    return {
                                        key: `period-${p.id}`,
                                        label: `${p.start.slice(0, 5)} ${p.end.slice(0, 5)}`,
                                        name: p.name,
                                    };
                                }),
                        );
                    });
            }

            axios.get("/student_absence_teacher/api/period_educ/")
                .then((resp) => {
                    this.educatorPeriods = resp.data.results
                        .filter(p => extractDayOfWeek(p.day_of_week).includes(currentDay));
                    if (this.pointOfView === "educator") {
                        this.fields = this.fields.concat(
                            this.educatorPeriods.map((p) => {
                                return {
                                    key: `period-${p.id}`,
                                    label: `${p.start.slice(0, 5)} ${p.end.slice(0, 5)}`,
                                    name: p.name,
                                };
                            }),
                        );
                    }
                });
        },
    },
    mounted: function () {
        this.get_absence_count();
    },
};
</script>
