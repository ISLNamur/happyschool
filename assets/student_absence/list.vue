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
                <b-card>
                    <filters
                        app="student_absence"
                        model="student_absence"
                        ref="filters"
                        @update="applyFilter"
                    />
                </b-card>
            </b-col>
        </b-row>
        <b-row align-h="between">
            <b-col
                cols="12"
                md="3"
                class="mt-1"
            >
                <b-pagination
                    :total-rows="entriesCount"
                    v-model="currentPage"
                    @change="changePage"
                    :per-page="20"
                />
            </b-col>
            <b-col
                cols="12"
                md="9"
                lg="7"
            >
                <b-row align-h="end">
                    <b-col
                        cols="12"
                        md="4"
                        v-if="proecoActivated"
                    >
                        <b-btn
                            :href="exportSelection"
                            target="_blank"
                            variant="outline-secondary"
                            class="w-100 mt-1"
                        >
                            <b-icon
                                icon="file-earmark"
                            />
                            Export ProEco
                        </b-btn>
                    </b-col>
                    <b-col
                        cols="12"
                        md="5"
                    >
                        <b-btn
                            variant="primary"
                            :pressed.sync="active"
                            class="w-100 mt-1"
                        >
                            <b-icon
                                icon="clipboard"
                            />
                            <span v-if="!active">Mes absences</span>
                            <span v-else>Toutes les absences</span>
                        </b-btn>
                    </b-col>
                </b-row>
            </b-col>
        </b-row>
        <b-row class="mt-1">
            <b-col>
                <absence-entry
                    v-for="absence in absences"
                    :key="absence.id"
                    :absence="absence"
                />
            </b-col>
        </b-row>
        <b-row v-if="entriesCount > 10">
            <b-col>
                <b-pagination
                    class="mt-2"
                    :total-rows="entriesCount"
                    v-model="currentPage"
                    @change="changePage"
                    :per-page="20"
                />
            </b-col>
        </b-row>
    </div>
</template>

<script>
import axios from "axios";

import AbsenceEntry from "./absence_entry.vue";
import Filters from "../common/filters.vue";
import {getFilters} from "../common/filters.js";

export default {
    data: function () {
        return {
            absences: [],
            active: false,
            showFilters: true,
            filter: "",
            currentPage: 1,
            entriesCount: 0,
            // eslint-disable-next-line no-undef
            proecoActivated: proeco,
        };
    },
    computed: {
        exportSelection: function () {
            return "/student_absence/api/export_selection/?page_size=1000" + this.filter;
        }
    },
    watch: {
        active: function (isActive) {
            if (isActive) {
                this.$store.commit("addFilter",
                    {filterType: "activate_last_absence", tag: "Activer", value: "true_activate_last_absence"}
                );
            } else {
                this.$store.commit("removeFilter", "activate_last_absence");
            }
            this.applyFilter();
        }
    },
    methods: {
        changePage: function (page) {
            this.currentPage = page;
            this.loadEntries();
            // Move to the top of the page.
            scroll(0, 0);
            return;
        },
        applyFilter: function () {
            this.filter = getFilters(this.$store.state.filters);
            this.loadEntries();
        },
        loadEntries: function () {
            let url = "/student_absence/api/student_absence/?ordering=-date_absence" + this.filter + "&page=" + this.currentPage;
            if (this.$store.state.forceAllAccess)
                url += "&forceAllAccess=1";
            axios.get(url)
                .then(response => {
                    this.entriesCount = response.data.count;
                    this.absences = response.data.results;
                });
        }
    },
    mounted: function () {
        this.applyFilter();
    },
    components: {
        AbsenceEntry,
        Filters,
    }
};
</script>
