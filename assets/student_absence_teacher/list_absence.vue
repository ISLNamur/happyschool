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
                <filters
                    app="student_absence_teacher"
                    model="absence"
                    ref="filters"
                    @update="applyFilter"
                    :show-search="showFilters"
                    @toggleSearch="showFilters = !showFilters"
                />
            </b-col>
        </b-row>
        <b-row>
            <b-col>
                <b-pagination
                    class="mt-1"
                    :total-rows="entriesCount"
                    v-model="currentPage"
                    @change="changePage"
                    :per-page="20"
                />
            </b-col>
        </b-row>
        <b-row>
            <b-col>
                <absence-entry
                    v-for="absence in absences"
                    :key="absence.id"
                    :absence="absence"
                    @filterStudent="filterStudent($event)"
                    @update="loadEntries()"
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
import Filters from "../common/filters_form.vue";
import {getFilters} from "../common/filters.js";

export default {
    data: function () {
        return {
            absences: [],
            latenesses: [],
            showFilters: true,
            filter: "",
            currentPage: 1,
            entriesCount: 0,
        };
    },
    methods: {
        filterStudent: function (matricule) {
            this.showFilters = true;
            this.$store.commit("addFilter",
                {filterType: "student__matricule", tag: matricule, value: matricule}
            );
            this.applyFilter();
        },
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
            axios.get("/student_absence_teacher/api/absence/?ordering=-date" + this.filter + "&page=" + this.currentPage)
                .then(resp => {
                    this.absences = resp.data.results;
                    this.entriesCount = resp.data.count;
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
