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
            <h2>Exclusion d'un élève</h2>
        </BCol>
    </BRow>
    <BRow>
        <BCol
            cols="12"
            md="3"
        >
            <BFormSelect
                text-field="display"
                value-field="id"
                :options="periods"
                v-model="period"
            />
        </BCol>
        <BCol
            sm="12"
            md="7"
        >
            <multiselect
                ref="input"
                :show-no-options="false"
                :internal-search="false"
                :options="searchOptions"
                @search-change="getSearchOptions"
                placeholder="Ajouter un étudiant"
                select-label=""
                selected-label="Sélectionné"
                deselect-label=""
                label="display"
                track-by="matricule"
                v-model="search"
            >
                <template #noResult>
                    Aucune personne trouvée.
                </template>
            </multiselect>
        </BCol>
        <BCol
            cols="3"
            sm="2"
            class="mt-1 mt-md-0"
        >
            <BButton
                :disabled="!search || addingStudent"
                @click="addStudent"
            >
                <BSpinner
                    v-if="addingStudent"
                    small
                />
                Ajouter
            </BButton>
        </BCol>
    </BRow>
    <BRow class="mt-2">
        <BCol
            sm="12"
            md="7"
            lg="5"
            class="d-flex justify-content-between align-items-center"
        >
            <IBiSearch class="me-1" />
            <multiselect
                :show-no-options="false"
                :internal-search="false"
                :options="searchOptions"
                @search-change="getSearchOptions"
                @select="getExclusions"
                @remove="getExclusions"
                placeholder="Rechercher un étudiant"
                select-label=""
                selected-label="Sélectionné"
                deselect-label=""
                label="display"
                track-by="matricule"
                v-model="filter"
            >
                <template #noResult>
                    Aucune personne trouvée.
                </template>
            </multiselect>
            <BButton
                :disabled="!filter"
                @click="filter=null;getExclusions()"
                class="ms-1"
            >
                <IBiX />
            </BButton>
        </BCol>
    </BRow>
    <BRow>
        <BTable
            stripped
            hover
            :items="exclusions"
            :fields="exclusionFields"
        >
            <template #cell(actions)="data">
                <BButton
                    size="sm"
                    variant="danger"
                    @click="removeExclusion(data.item, data.index)"
                >
                    <IBiTrash />
                </BButton>
            </template>
        </BTable>
    </BRow>
    <BRow>
        <BCol>
            <BPagination
                :total-rows="entriesCount"
                v-model="currentPage"
                @update:model-value="changePage"
            />
        </BCol>
    </BRow>
</template>

<script>
import Multiselect from "vue-multiselect";
import "vue-multiselect/dist/vue-multiselect.css";

import axios from "axios";

import { useModalController } from "bootstrap-vue-next";

import { studentAbsenceTeacherStore } from "./stores/index.js";

import { displayStudent } from "@s:core/js/common/utilities";

const token = { xsrfCookieName: "csrftoken", xsrfHeaderName: "X-CSRFToken"};

export default {
    setup: function () {
        const { confirm } = useModalController();
        return { confirm };
    },
    data: function () {
        return {
            periods: [],
            period: null,
            exclusions: [],
            exclusionFields: [
                {
                    key: "dateExclusion",
                    label: "Date d'exclusion"
                },
                {
                    key: "studentName",
                    label: "Nom",
                },
                {
                    key: "period",
                    label: "Période",
                },
                {
                    key: "count",
                    label: "Exclusions",
                },
                {
                    key: "actions",
                    label: "",
                }
            ],
            search: "",
            searchOptions: [],
            searchId: 0,
            filter: null,
            addingStudent: false,
            currentPage: 1,
            entriesCount: 20,
            store: studentAbsenceTeacherStore(),
        };
    },
    methods: {
        displayStudent,
        changePage: function (page) {
            this.currentPage = page;
            this.getExclusions();
            // Move to the top of the page.
            scroll(0, 0);
            return;
        },
        removeExclusion: function (item, idx) {
            console.log(item, idx);
            this.confirm({props: {
                body: "Êtes-vous sûr de vouloir supprimer cette exclusion ?",
                centered: true,
                buttonSize: "sm",
                okVariant: "danger",
                okTitle: "Oui",
                cancelTitle: "Annuler",
            }})
                .then(remove => {
                    if (!remove) return;

                    axios.delete(`/student_absence_teacher/api/absence_teacher/${item.id}/`, token)
                        .then(() => {
                            this.getExclusions();
                        });
                });
        },
        getSearchOptions: function (query) {
            // Ensure the last search is the first response.
            this.searchId += 1;
            let currentSearch = this.searchId;

            const data = {
                query: query,
                teachings: this.store.teachings,
                people: "student",
                check_access: false,
            };
            axios.post("/annuaire/api/people/", data, token)
                .then(response => {
                    if (this.searchId !== currentSearch)
                        return;
                
                    this.searchOptions = response.data;
                });
        },
        selectStudent: function (matricule) {
            axios.get("/annuaire/api/student/" + matricule + "/")
                .then(resp => {
                    if (resp.data) {
                        this.search = resp.data;
                        this.addStudent();
                    }
                })
                .catch(() => {
                    console.log("Aucun étudiant trouvé");
                    this.addingStudent = false;
                });
        },
        addStudent: function () {
            axios.post(
                "/student_absence_teacher/api/exclude_student/",
                {student_id: this.search.matricule, period_id: this.period},
                token
            )
                .then(() => {
                    this.search = null;
                    this.getExclusions();
                });
        },
        getExclusions: function () {
            const studentFilter = this.filter ? `&student__matricule=${this.filter.matricule}` : "";
            axios.get(`/student_absence_teacher/api/absence_teacher/?status=excluded&page=${this.currentPage}&ordering=-date_absence${studentFilter}`)
                .then((resp) => {
                    this.exclusions = resp.data.results.map(e => {
                        return {
                            id: e.id,
                            dateExclusion: e.date_absence,
                            studentName: this.displayStudent(e.student),
                            period: `${e.period.start.slice(0, 5)} - ${e.period.end.slice(0, 5)}`,
                            count: e.excluded_count,
                        };
                    });
                    this.entriesCount = resp.data.count;
                });
        },
        overloadInput: function () {
            setTimeout(() => {
                // Check if input is loaded.
                let refInput = this.$refs.input;
                if (refInput) {
                    let input = refInput.$refs.search;
                    input.focus();
                    input.addEventListener("keypress", (e) => {
                        if (e.key == "Enter") {
                            if (refInput.search && refInput.search.length > 1 && !isNaN(refInput.search)) {
                                this.selectStudent(refInput.search);
                                refInput.search = "";
                            }
                        }
                    });
                    return input;
                } else {
                    this.overloadInput();
                }
            }, 300);
            
        },
    },
    mounted: function () {
        this.overloadInput();
        this.getExclusions();
        axios.get("/student_absence_teacher/api/period_teacher/")
            .then((resp) => {
                this.periods = resp.data.results;
            });
    },
    components: {
        Multiselect,
    }
};
</script>
