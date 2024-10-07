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
            <h2>Exclusion d'un élève</h2>
        </b-col>
    </b-row>
    <b-row>
        <b-col
            cols="12"
            md="3"
        >
            <b-select
                text-field="display"
                value-field="id"
                :options="periods"
                v-model="period"
            />
        </b-col>
        <b-col
            sm="12"
            md="7"
        >
            <multiselect
                ref="input"
                :show-no-options="false"
                :internal-search="false"
                :options="searchOptions"
                @search-change="getSearchOptions"
                :loading="searchLoading"
                placeholder="Rechercher un étudiant"
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
        </b-col>
        <b-col
            cols="3"
            sm="2"
            class="mt-1 mt-md-0"
        >
            <b-button
                :disabled="!search || addingStudent"
                @click="addStudent"
            >
                <b-spinner
                    v-if="addingStudent"
                    small
                />
                Ajouter
            </b-button>
        </b-col>
    </b-row>
    <b-row>
        <b-table
            stripped
            hover
            :items="exclusions"
            :fields="exclusionFields"
        />
    </b-row>
</template>

<script>
import Vue from "vue";
import { BootstrapVue, BootstrapVueIcons } from "bootstrap-vue";
import "bootstrap-vue/dist/bootstrap-vue.css";

Vue.use(BootstrapVue);
Vue.use(BootstrapVueIcons);

import Multiselect from "vue-multiselect";
import "vue-multiselect/dist/vue-multiselect.css";

import axios from "axios";

import { studentAbsenceTeacherStore } from "./stores/index.js";

const token = { xsrfCookieName: "csrftoken", xsrfHeaderName: "X-CSRFToken"};

export default {
    data: function () {
        return {
            periods: [],
            period: null,
            exclusions: [],
            search: "",
            searchOptions: [],
            searchId: 0,
            addingStudent: false,
            store: studentAbsenceTeacherStore(),
        };
    },
    methods: {
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
            axios.get("/student_absence_teacher/api/absence_teacher/?status=excluded")
                .then((resp) => {
                    this.exclusions = resp.data.results.map(e => {
                        return {
                            dateExclusion: e.date_absence,
                            studentName: `${e.student.last_name} ${e.student.first_name}`,
                            period: `${e.period.start.slice(0, 5)} - ${e.period.end.slice(0, 5)}`,
                        };
                    });
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
        Multiselect
    }
};
</script>
