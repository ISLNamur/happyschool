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
        <b-container v-if="loaded">
            <b-row>
                <h2>Infirmerie</h2>
            </b-row>
            <b-row>
                <b-col
                    cols="12"
                    md="4"
                    lg="3"
                >
                    <b-button
                        variant="outline-success"
                        to="/new/"
                        class="w-100"
                    >
                        <b-icon
                            icon="plus"
                            scale="1.5"
                        />
                        Ajouter un malade
                    </b-button>
                </b-col>
                <b-col
                    cols="12"
                    lg="9"
                >
                    <filters
                        app="infirmerie"
                        model="passage"
                        ref="filters"
                        :store="store"
                        :show-search="showSearch"
                        @toggleSearch="showSearch = !showSearch"
                        @update="applyFilter"
                        class="mt-1 mt-lg-0"
                    />
                </b-col>
            </b-row>
            <b-pagination
                class="mt-1"
                :total-rows="entriesCount"
                v-model="currentPage"
                @change="changePage"
                :per-page="20"
            />
            <infirmerie-entry
                v-for="(entry, index) in entries"
                :key="entry.id"
                :row-data="entry"
                @delete="askDelete(entry)"
                @edit="editEntry(index, false)"
                @sortie="editEntry(index, true)"
                @filterStudent="filterStudent($event)"
                @showInfo="showInfo(entry)"
            />
        </b-container>
        <b-modal
            ref="deleteModal"
            cancel-title="Annuler"
            hide-header
            centered
            @ok="deleteEntry"
            @cancel="currentEntry = null"
            :no-close-on-backdrop="true"
            :no-close-on-esc="true"
        >
            Êtes-vous sûr de vouloir supprimer ce passage ?
        </b-modal>
    </div>
</template>

<script>
import Filters from "@s:core/js/common/filters_form.vue";

import axios from "axios";

import InfirmerieEntry from "./infirmerieEntry.vue";

import { infirmerieStore } from "./stores/index.js";

export default {
    data: function () {
        return {
            loaded: false,
            currentPage: 1,
            filter: "",
            ordering: "&ordering=-datetime_arrive",
            currentEntry: null,
            entries: [],
            entriesCount: 0,
            inputStates: {
                "name": null,
            },
            showSearch: false,
            store: infirmerieStore(),
        };
    },
    computed: {
        currentName: function () {
            return "";
        }
    },
    methods: {
        changePage: function (page) {
            this.currentPage = page;
            this.loadEntries();
        },
        openModal: function (sortie) {
            this.$refs.addPassageModal.show(sortie);
        },
        showInfo: function (entry) {
            this.currentEntry = entry;
            this.$refs.infoModal.show();
        },
        filterStudent: function (matricule) {
            this.showSearch = true;
            this.store.addFilter(
                {filterType: "matricule_id", tag: matricule, value: matricule}
            );
            this.applyFilter();
        },
        applyFilter: function () {
            this.filter = "";
            let storeFilters = this.store.filters;
            for (let f in storeFilters) {
                if (storeFilters[f].filterType.startsWith("date")
                    || storeFilters[f].filterType.startsWith("time")) {
                    let ranges = storeFilters[f].value.split("_");
                    this.filter += "&" + storeFilters[f].filterType + "__gt=" + ranges[0];
                    this.filter += "&" + storeFilters[f].filterType + "__lt=" + ranges[1];
                } else {
                    this.filter += "&" + storeFilters[f].filterType + "=" + storeFilters[f].value;
                }
            }
            this.currentPage = 1;
            this.loadEntries();
        },
        askDelete: function (entry) {
            this.currentEntry = entry;
            this.$refs.deleteModal.show();
        },
        deleteEntry: function () {
            const token = { xsrfCookieName: "csrftoken", xsrfHeaderName: "X-CSRFToken"};
            axios.delete("/infirmerie/api/passage/" + this.currentEntry.id, token)
                .then(() => {
                    this.loadEntries();
                });

            this.currentEntry = null;
        },
        editEntry: function(index, sortie) {
            this.currentEntry = this.entries[index];
            this.openModal(sortie);
        },
        loadEntries: function () {
            axios.get("/infirmerie/api/passage/?page=" + this.currentPage + this.filter + this.ordering)
                .then(response => {
                    this.entries = response.data.results;
                    this.entriesCount = response.data.count;
                    this.loaded = true;
                });
        },
    },
    mounted: function() {
        this.applyFilter();
    },
    components: {
        "filters": Filters,
        "infirmerie-entry": InfirmerieEntry,
    },
};
</script>
<style>
.loading {
    content: " ";
    display: block;
    position: absolute;
    width: 80px;
    height: 80px;
    background-image: url(/static/img/spin.svg);
    background-size: cover;
    left: 50%;
    top: 50%;
}
</style>
