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
        <b-row class="mb-1">
            <b-col
                cols="12"
                md="8"
            >
                <b-form
                    inline
                    class="mb-1"
                >
                    <b-form-group
                        label="Date"
                        class="mr-2"
                    >
                        <b-overlay
                            :show="loading"
                            rounded="sm"
                        >
                            <b-input
                                type="date"
                                v-model="date"
                                @input="get_absence_count"
                            />
                        </b-overlay>
                    </b-form-group>
                    <b-form-group
                        label="Rechercher"
                    >
                        <multiselect
                            ref="input"
                            :show-no-options="false"
                            :internal-search="false"
                            :options="searchOptions"
                            @search-change="getSearchOptions"
                            placeholder="Une classe, un élève,…"
                            select-label=""
                            selected-label="Sélectionné"
                            deselect-label=""
                            label="display"
                            track-by="id"
                            v-model="search"
                            @select="selected"
                        >
                            <span slot="noResult">Aucune personne trouvée.</span>
                            <span slot="noOptions" />
                        </multiselect>
                    </b-form-group>
                </b-form>
            </b-col>
            <b-col>
                <b-button
                    v-b-toggle.other-options
                    variant="primary"
                >
                    <b-icon icon="grid1x2" />
                    Autres vues
                </b-button>
            </b-col>
        </b-row>
        <b-row>
            <b-col>
                <b-table
                    hover
                    bordered
                    :items="absence_count"
                    :fields="fields"
                    :filter="filter"
                    :filter-included-fields="['classe']"
                >
                    <template #head(classe)="">
                        <b-form-group
                            label-for="filterInput"
                        >
                            <b-form-input
                                v-model="filter"
                                type="search"
                                id="filterInput"
                                placeholder="Filtrer par classe"
                            />
                        </b-form-group>
                    </template>
                    <template #cell(classe)="data">
                        <b-link :to="`/class_view/${data.item.classe__id}/${date}/`">
                            {{ data.value }}
                        </b-link>
                    </template>
                    <template #cell()="data">
                        <span
                            v-if="data.value.teacher_count >= 0"
                        >
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
                        :href="`/student_absence/api/export_selection/?page_size=2000&date_absence=${date}&period__name=${p.name}&is_absent=true${exportOwnClasses}`"
                    >
                        {{ p.name }}
                    </b-dropdown-item>
                    <b-dropdown-item
                        :href="`/student_absence/api/export_selection/?page_size=2000&date_absence=${date}&is_absent=true${exportOwnClasses}`"
                    >
                        Toute la journée
                    </b-dropdown-item>
                </b-dropdown>
            </b-form-group>
        </b-sidebar>
    </div>
</template>

<script>
import axios from "axios";

import Moment from "moment";
Moment.locale("fr");


import Multiselect from "vue-multiselect";
import "vue-multiselect/dist/vue-multiselect.min.css";

export default {
    data: function () {
        return {
            date: Moment().format("YYYY-MM-DD"),
            pointOfView: "teacher",
            optionsPointOfView: [
                { text: "Prof.", value: "teacher"},
                { text: "Éduc.", value: "educator"},
            ],
            classListType: "ownclass",
            optionsClassListType: [
                { text: "Ses classes", value: "ownclass"},
                { text: "Toutes", value: "allclass"},
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
    methods: {
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
            this.fields = [{key: "classe", }];
            if (this.pointOfView === "teacher") {
                axios.get("/student_absence_teacher/api/period/")
                    .then(resp => {
                        this.fields = this.fields.concat(
                            resp.data.results.map(p => {
                                return {
                                    key: `period-${p.id}`,
                                    label: `${p.start.slice(0, 5)} ${p.end.slice(0, 5)}`,
                                    name: p.name
                                };
                            })
                        );
                    });
            }
            axios.get("/student_absence/api/period/")
                .then(resp => {
                    this.educatorPeriods = resp.data.results;
                    if (this.pointOfView === "educator") {
                        this.fields = this.fields.concat(
                            resp.data.results.map(p => {
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
        selected: function (option) {
            if (option.type == "classe") {
                // reroute to classe
                this.$router.push(`/class_view/${option.id}/${this.date}/`);
                return;
            } else {
                // reroute to student
            }
        }, 
        getSearchOptions: function (query) {
            // Ensure the last search is the first response.
            this.searchId += 1;
            let currentSearch = this.searchId;

            const token = { xsrfCookieName: "csrftoken", xsrfHeaderName: "X-CSRFToken"};
            const data = {
                query: query,
                teachings: this.$store.state.settings.teachings,
                people: "student",
                check_access: this.classListType === "ownclass",
            };
            axios.post("/annuaire/api/people_or_classes/", data, token)
                .then(response => {
                    if (this.searchId !== currentSearch)
                        return;

                    const options = response.data.map(p => {
                        if (Number.isNaN(Number.parseInt(query[0]))) {
                            return {
                                display: p.display,
                                id: p.matricule,
                                type: "student",
                            };
                        } else {
                        // It is a classe.
                            let classe = p;
                            classe.type = "classe";
                            return classe;
                        }
                    });

                    this.searchOptions = options;
                });
        },
    },
    mounted: function () {
        this.get_absence_count();
    },
    components: {
        Multiselect
    }
};
</script>
