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
    <b-row>
        <b-col>
            <b-overlay :show="loading">
                <b-table
                    hover
                    bordered
                    :items="absence_count"
                    :fields="fields"
                    :filter="filter"
                    :filter-included-fields="['classe']"
                >
                    <template #head(classe)="">
                        <div class="d-flex justify-content-between">
                            <b-button
                                v-b-toggle.other-options
                                variant="primary"
                                class="mr-1"
                            >
                                <b-icon icon="grid1x2" />
                            </b-button>

                            <b-form-group label-for="filterInput">
                                <b-form-input
                                    v-model="filter"
                                    type="search"
                                    id="filterInput"
                                    placeholder="Filtrer par classe"
                                />
                            </b-form-group>
                        </div>
                    </template>
                    <template #cell(classe)="data">
                        <b-link :to="`/overview/${date}/class_view/${data.item.classe__id}/`">
                            {{ data.value }}
                        </b-link>
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
                </b-table>
            </b-overlay>
        </b-col>
    </b-row>
    <b-sidebar
        id="other-options"
        title="Options de visualisation"
        right
        shadow
    >
        <b-form-group
            label="Vue horaire"
            v-slot="{ ariaDescribedby }"
            class="ml-1"
        >
            <b-form-radio-group
                id="point-of-view-radio"
                v-model="pointOfView"
                :options="optionsPointOfView"
                :aria-describedby="ariaDescribedby"
                button-variant="outline-primary"
                name="point-of-view-radio"
                @change="get_absence_count()"
                buttons
            />
        </b-form-group>
        <b-form-group
            label="Liste des classes"
            v-slot="{ ariaDescribedby }"
            class="ml-1"
        >
            <b-form-radio-group
                id="class-list-type-radio"
                v-model="classListType"
                :options="optionsClassListType"
                :aria-describedby="ariaDescribedby"
                button-variant="outline-primary"
                name="class-list-type-radio"
                @change="get_absence_count()"
                buttons
            />
        </b-form-group>
        <b-form-group
            v-if="isProecoActivated"
            label="Export vers ProEco"
            class="ml-1"
        >
            <b-dropdown
                text="Export"
                variant="outline-secondary"
            >
                <b-dropdown-item
                    v-for="p in educatorPeriods"
                    :key="p.id"
                    :href="`/student_absence_teacher/api/export_selection/?page_size=2000&date_absence=${date}&period__name=${p.name}&status=A${exportOwnClasses}`"
                >
                    {{ p.name }}
                </b-dropdown-item>
                <b-dropdown-item
                    :href="`/student_absence_teacher/api/export_selection/?page_size=2000&date_absence=${date}&status=A${exportOwnClasses}`"
                >
                    Toute la journée
                </b-dropdown-item>
            </b-dropdown>
        </b-form-group>
    </b-sidebar>
</template>

<script>
import axios from "axios";

import Moment from "moment";
import "moment/dist/locale/fr";
Moment.locale("fr");

import { extractDayOfWeek } from "@s:core/js/common/utilities.js";

import { studentAbsenceTeacherStore } from "./stores/index.js";

export default {
    props: {
        date: {
            type: String,
            default: () => Moment().format("YYYY-MM-DD")
        }
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
            searchOptions: [],
            search: "",
            searchId: -1,
            store: studentAbsenceTeacherStore()
        };
    },
    computed: {
        isProecoActivated: function () {
            // eslint-disable-next-line no-undef
            return proeco;
        },
        exportOwnClasses: function () {
            return this.classListType === "ownclass" ? "&activate_own_classes=true" : "";
        }
    },
    watch: {
        date: function () {
            this.get_absence_count();
        }
    },
    methods: {
        changeDate: function (evt) {
            this.$router.push(`/overview/${evt}/`);
        },
        get_absence_count: function () {
            this.loading = true;
            this.getPeriods();
            axios.get(`/student_absence_teacher/api/count_absence/${this.date}/${this.pointOfView}/${this.classListType}/`)
                .then(resp => {
                    this.absence_count = JSON.parse(resp.data).map(row => {
                        const periods = Object.entries(row).filter(c => c[0].startsWith("period"));
                        const emptyPeriods = periods.filter(p => p[1]["teacher_count"] < 0);
                        row._cellVariants = emptyPeriods.reduce((acc, v) => {
                            acc[v[0]] = "warning";
                            return acc;
                        }, {});
                        if (periods.length > 0 && "not_teacher_count" in periods[0][1]) {
                            const mismatchPeriods = periods.filter(p => {
                                if (p[1]["not_teacher_count"] < 0 || p[1]["teacher_count"] < 0) {
                                    return false;
                                }
                                if (p[1]["not_teacher_count"] != p[1]["teacher_count"]) {
                                    return true;
                                }
                                return false;
                            });
                            mismatchPeriods.forEach(p => {
                                row._cellVariants[p[0]] = "danger";
                            });
                        }
                        return row;
                    });
                    this.loading = false;
                });
        },
        getPeriods: function () {
            this.fields = [{ key: "classe", }];
            const currentDay = (new Date(this.date)).getDay();

            if (this.pointOfView === "teacher") {
                axios.get("/student_absence_teacher/api/period_teacher/")
                    .then(resp => {
                        this.fields = this.fields.concat(
                            resp.data.results
                                .filter(p => extractDayOfWeek(p.day_of_week).includes(currentDay))
                                .map(p => {
                                    return {
                                        key: `period-${p.id}`,
                                        label: `${p.start.slice(0, 5)} ${p.end.slice(0, 5)}`,
                                        name: p.name
                                    };
                                })
                        );
                    });
            }

            axios.get("/student_absence_teacher/api/period_educ/")
                .then(resp => {
                    this.educatorPeriods = resp.data.results
                        .filter(p => extractDayOfWeek(p.day_of_week).includes(currentDay));
                    if (this.pointOfView === "educator") {
                        this.fields = this.fields.concat(
                            this.educatorPeriods.map(p => {
                                return {
                                    key: `period-${p.id}`,
                                    label: `${p.start.slice(0, 5)} ${p.end.slice(0, 5)}`,
                                    name: p.name
                                };
                            })
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
